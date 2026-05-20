from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'laundrynow_secret_key_for_flash_messages'
DATABASE = 'laundry.db'

def get_db_connection():
    """建立並傳回一個資料庫連接，結果以 Row 形式呈現，方便用欄位名稱取值"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """首頁：顯示所有洗衣機的即時狀態與剩餘時間"""
    conn = get_db_connection()
    # 按照洗衣機編號排序
    machines = conn.execute('SELECT * FROM laundry ORDER BY machine_number').fetchall()
    conn.close()
    return render_template('index.html', machines=machines)

@app.route('/report', methods=['GET', 'POST'])
def report():
    """回報路由：支援 GET (顯示表單) 與 POST (提交回報資料)"""
    conn = get_db_connection()
    
    if request.method == 'POST':
        # 1. 獲取表單傳入的 id 或 machine_number
        machine_id = request.form.get('machine_id')
        machine_number = request.form.get('machine_number')
        status = request.form.get('status')
        
        # 驗證必要欄位是否有填寫
        if not (machine_id or machine_number) or not status:
            flash('請提供洗衣機識別資料與回報狀態！', 'error')
            conn.close()
            return redirect(url_for('report'))
            
        # 驗證狀態值是否合法
        valid_statuses = ['空閒', '使用中', '故障']
        if status not in valid_statuses:
            flash(f'不合法的狀態值：{status}。只能填入「空閒」、「使用中」或「故障」！', 'error')
            conn.close()
            return redirect(url_for('report'))
        
        # 2. 自動計算剩餘時間 (remaining_time)
        # 規則：如果狀態為 '空閒' 或 '故障'，剩餘時間自動歸零；若為 '使用中' 則取輸入值，預設為 30 分鐘。
        if status in ['空閒', '故障']:
            remaining_time = 0
        else:
            try:
                remaining_time = int(request.form.get('remaining_time', 30))
                if remaining_time < 0:
                    remaining_time = 0
            except (ValueError, TypeError):
                remaining_time = 30  # 輸入不合法時預設 30 分鐘
        
        try:
            # 3. 更新 SQLite 資料庫
            if machine_id:
                # 優先使用 ID 更新
                result = conn.execute('''
                    UPDATE laundry 
                    SET status = ?, remaining_time = ?, updated_at = datetime('now', 'localtime')
                    WHERE id = ?
                ''', (status, remaining_time, machine_id))
            else:
                # 否則使用 machine_number 更新
                result = conn.execute('''
                    UPDATE laundry 
                    SET status = ?, remaining_time = ?, updated_at = datetime('now', 'localtime')
                    WHERE machine_number = ?
                ''', (status, remaining_time, machine_number))
                
            conn.commit()
            
            # 檢查是否有實際更新到資料
            if result.rowcount > 0:
                flash(f'更新成功！已將設備狀態更新為「{status}」，剩餘時間：{remaining_time} 分鐘。', 'success')
            else:
                flash('找不到指定的洗衣機設備，更新失敗。', 'error')
                
        except sqlite3.Error as e:
            flash(f'資料庫更新出錯：{str(e)}', 'error')
        finally:
            conn.close()
            
        # 4. 重新導向回首頁
        return redirect(url_for('index'))
        
    # GET 請求：顯示回報表單頁面
    machines = conn.execute('SELECT id, machine_number, location, status FROM laundry ORDER BY machine_number').fetchall()
    conn.close()
    
    # 支援從首頁直接帶入要回報的 machine_id
    preselected_id = request.args.get('machine_id')
    return render_template('report.html', machines=machines, preselected_id=preselected_id)

if __name__ == '__main__':
    # 如果資料庫尚未初始化，自動執行初始化
    if not os.path.exists(DATABASE):
        from init_db import init_db
        init_db()
        
    print("啟動 LaundryNow 宿舍洗衣機即時狀態查詢系統...")
    app.run(debug=True, port=5000)

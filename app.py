import time
import random 
import tempfile
from tkinter import *
from tkinter import filedialog, messagebox
from tkinter import ttk
from time import strftime
from datetime import datetime, date 
from db import Database



bg_color = "#c7c7c7"
blue_color = "#4b8598"
white_color = "white"
grey_color = "gray"
red_color = "red"
green_color = "green"
purple_color = "#4f234f"


db =  Database('product_database.db')
root = Tk() 


def move_window(event):
    root.geometry('+{0}+{0}'.format(event.x_root, y_root))


# 
class HomePageView(object):
    
    def about_message(self):
        msg = """
        Owner: Angono Derkos\n
        App Type: Product Management System\n
        Built Date: May 2022\n
        Vesion: 1.0\n
        Developer: Denamse Angono Derkos Tirel\n
        Email: tirelangono@gmail.com\n"""
        messagebox.showinfo("About System", msg)

    def exit_app(self):
        sure = messagebox.askyesno("Exit","Are you sure you want to exit?", parent=self.root)
        if sure == True:
            global root
            root.quit()


    def __init__(self, root):
        self.root = root
        self.root.title("Mega Product")
        self.root.geometry('1000x550+0+0')
        self.root.config(bd=0, bg=white_color, relief='flat')
        # self.root.state('zoomed')

        product_ref_code = StringVar()
        product_name = StringVar()
        product_unit_price = StringVar()
        product_quantity = StringVar()
        product_total_price = StringVar()
        created_on = StringVar()

        def getData(event):
            selected_row = tv.focus()
            data = tv.item(selected_row) 
            global row 
            row = data["values"]
            product_ref_code.set(row[1])
            product_name.set(row[2])
            product_unit_price.set(row[3])
            product_quantity.set(row[4])
            product_total_price.set(row[5])
            created_on.set(row[6])


        def add_product_data():
            if entry_product_ref_code.get()=="" or entry_product_name.get()=="" or entry_product_unit_price.get()=="" or entry_product_quantity.get()=="" or entry_product_total_price.get()=="" or entry_created_on.get()=="":
                messagebox.showerror("Error in Inputs", "Please Fill All the Details", parent=root) 
                return 
            db.insert_products(entry_product_ref_code.get(),entry_product_name.get(),entry_product_unit_price.get(),entry_product_quantity.get(),entry_product_total_price.get(),entry_created_on.get())
            messagebox.showinfo("Success!", "Product Has Been Successfully Saved", parent=root)
            clearAll() 
            displayAll()

        def update_product_data():
            if entry_product_ref_code.get()=="" or entry_product_name.get()=="" or entry_product_unit_price.get()=="" or entry_product_quantity.get()=="" or entry_product_total_price.get()=="" or entry_created_on.get()=="":
                messagebox.showerror("Error in Inputs", "Please Fill All the Details", parent=root) 
                return 
            db.update_products(row[0], entry_product_ref_code.get(),entry_product_name.get(),entry_product_unit_price.get(),entry_product_quantity.get(),entry_product_total_price.get(),entry_created_on.get())
            messagebox.showinfo("Success!", "Record Has Been Successfully Updated", parent=root)
            clearAll() 
            displayAll()


        def get_ref_code():
          get_ref = random.randint(100000, 99999999)
          product_ref_code.set(get_ref)

        get_ref_code()


        def delete_product_data():
            messagebox.showinfo("Delete", "Are you sure you want to delete these data?", parent=root)
            db.remove_products(row[0])
            clearAll() 
            displayAll()
            get_ref_code()


        def clearAll():
            product_ref_code.set("")
            product_name.set("")
            product_unit_price.set("")
            product_quantity.set("")
            product_total_price.set("")
            displayAll()
            get_ref_code() 

        def displayAll():
            tv.delete(*tv.get_children()) 
            for row in db.fetch_products():
                tv.insert("", END, values=row)

        def search_product_data():
            tv.delete(*tv.get_children()) 
            if entry_product_name.get() or entry_product_unit_price.get() or entry_product_quantity.get() or entry_product_total_price.get():
                for row in db.search_products(entry_product_name.get(),entry_product_unit_price.get(),entry_product_quantity.get(),entry_product_total_price.get()):
                    tv.insert("", END, values=row)
            else:
                messagebox.showerror("Error","This product does not exist.", parent=root)
                displayAll() 

        def get_total_cost_data():
            try:
                u_price = entry_product_unit_price.get()
                qty = entry_product_quantity.get()
                total_amount = float(u_price) * float(qty)
                product_total_price.set(total_amount)
            except:
                messagebox.showinfo("Info","Nothing to calculate", parent=root)


        # =======================frames==========================
        top_frame = LabelFrame(self.root, relief='raised', bg=bg_color, height=80, pady=5)
        top_frame.pack(side='top', fill='x', expand='false')
        
        decoration_frame = LabelFrame(self.root, bg=blue_color, height=10, width=1600)
        decoration_frame.pack(pady=1, fill='x', expand='false')

        bottom_frame = LabelFrame(self.root, padx=5, bg=white_color, width=1600, relief='flat')
        bottom_frame.pack(pady=1)

        # items 1 frame
        booking_fields = LabelFrame(bottom_frame, pady=5, padx=10, bg=white_color, width=500,)
        booking_fields.pack(side='left', pady=1, fill='y', expand='false')

        # items 2 frame
        list_frame = LabelFrame(bottom_frame, pady=5, padx=10, bg=white_color, width=500,)
        list_frame.pack(side='right', pady=1, fill='y', expand='false')


        # labels headers
        header1_title = Label(top_frame, 
            text='MEGA PRODUCT', 
            font=('arial', 30, 'bold'), 
            fg=purple_color, 
            bg=bg_color)
        header1_title.pack(side=TOP)

        header2_title = Label(top_frame, 
            text='SIMPLE AND FAST TO USE.', 
            font=('arial', 14, 'bold'), 
            fg=green_color, 
            bg=bg_color)
        header2_title.pack()
        
        '''
        ##############List Info###############
        '''

        customer_frame = LabelFrame(list_frame, pady=5, bg=white_color, width=300, relief='flat')
        customer_frame.pack(side='top', anchor='w',  fill='x')


        about_btn = Button(customer_frame, 
            text="About",  
            bg=grey_color, 
            fg=white_color,
            relief='flat',
            width=14,
            bd=1,
            activeforeground=white_color,
            activebackground=blue_color,
            font=('arial',12, 'bold'),
            command=self.about_message)
        about_btn.grid(row=0, column=0, padx=2)

        exit_btn = Button(customer_frame, 
            text="Exit",  
            bg=red_color, 
            fg=white_color,
            relief='flat',
            width=14,
            bd=1,
            activeforeground=white_color,
            activebackground=blue_color,
            font=('arial',12,'bold'),
            command=self.exit_app)
        exit_btn.grid(row=0, column=1, padx=2)

        def get_count():
            for row in db.count_product():
                print(row)
                count_items.config(text=f'{row} items')

        count_items = Label(customer_frame,
            font=('arial', 14, 'bold'),
            fg=green_color, 
            bg=white_color)
        count_items.grid(row=0, column=2, padx=2)

        get_count()

        # list frame
        tree_frame = Frame(list_frame, bg=white_color)
        tree_frame.pack(pady=10)

        # styling
        style = ttk.Style(root)
        style.theme_use('default')
        style.configure("Treeview", 
            background="silver", 
            foreground="#4f234f", 
            rowheight=32, 
            fieldbackground="silver", 
            font=('arial', 14))
        style.map('Treeview', background=[('selected', '#4b8598')], foreground=[('selected', 'white')])

        # list scroll bar
        tree_scroll_vertical = Scrollbar(tree_frame, orient='vertical')
        tree_scroll_vertical.pack(side=RIGHT, fill='y') 
        tree_scroll_horizontal = Scrollbar(tree_frame, orient='horizontal')
        tree_scroll_horizontal.pack(side=BOTTOM, fill='x') 

        # create the Treeview 
        tv = ttk.Treeview(tree_frame, 
            yscrollcommand=tree_scroll_vertical.set,
            xscrollcommand=tree_scroll_horizontal.set,  
            selectmode="extended",
            columns=(1,2,3,4,5,6,7))
        tv.pack()

        # configure the Scrollbar 
        tree_scroll_vertical.config(command=tv.yview) 
        tree_scroll_horizontal.config(command=tv.xview) 

        # columns 
        tv['columns'] = (
            "ID", 
            "Ref Code",
            "Product Name",
            "Unit Price",
            "Quantity",
            "Total Price",
            "Date")

        # format our columns
        tv.column("ID", width=90, anchor='center')
        tv.column("Ref Code", width=200, anchor='center')
        tv.column("Product Name", width=260, anchor='center')
        tv.column("Unit Price", width=200, anchor='center')
        tv.column("Quantity", width=200, anchor='center')
        tv.column("Total Price", width=200, anchor='center')
        tv.column("Date", width=260, anchor='center')
        
        # create headings 
        tv.heading('ID', text="ID",)
        tv.heading('Ref Code', text="Ref Code",)
        tv.heading('Product Name', text="Product Name",)
        tv.heading('Unit Price', text="Unit Price ($)",)
        tv.heading('Quantity', text="Quantity",)
        tv.heading('Total Price', text="Total Price ($)",)
        tv.heading('Date', text="Date",)
        tv['show'] = 'headings'
        tv.bind("<ButtonRelease-1>", getData)
        tv.pack(fill='x')

        # create Striped Row Tags 
        tv.tag_configure('oddrow', background='white', foreground='black')
        tv.tag_configure('evenrow', background='lightblue', foreground='black')

        # add our data to the screen 
        global count 
        count = 0 

        for record in db.fetch_products():
            if count%2 == 0:
                tv.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6]), tags=('evenrow',))
            else: 
                tv.insert(parent='', index='end', iid=count, text='', values=(record[0],record[1],record[2],record[3],record[4],record[5],record[6]), tags=('oddrow',))
            # increment counter 
            count +=1 

        displayAll()


        '''
        ==================Fields=================
        '''

        # add staff label
        txt_title = Label(booking_fields, 
          text='Add New Product', 
          font=('arial', 16,'bold'), 
          fg='#4b8598', 
          bg=white_color)
        txt_title.grid(row=0, column=0, columnspan=2, pady=10, sticky='w')

        # product_ref_code
        lab_product_ref_code = Label(booking_fields, 
          text='Ref Code: ', 
          padx=2, 
          pady=2, 
          font=('arial', 12, 'bold'), 
          fg='grey', 
          bg=white_color)
        lab_product_ref_code.grid(row=1, column=0,sticky='w')
        entry_product_ref_code = Entry(booking_fields, 
          bg='white', 
          width=20, 
          font=('arial', 12, 'bold'),
          bd=2,
          textvariable=product_ref_code)
        entry_product_ref_code.grid(row=1, column=1) 

        # product_name
        lab_product_name = Label(booking_fields, 
          text='Product Name: ', 
          padx=2, 
          pady=2, 
          font=('arial', 12, 'bold'), 
          fg='grey', 
          bg=white_color)
        lab_product_name.grid(row=2, column=0, sticky='w')
        entry_product_name = Entry(booking_fields, 
          bg='white', 
          width=20, 
          font=('arial',12, 'bold'), 
          bd=2,
          textvariable=product_name)
        entry_product_name.grid(row=2, column=1)  

        # product_unit_price
        lab_product_unit_price = Label(booking_fields, 
          text='Unit Price ($): ', 
          padx=2, 
          pady=2, 
          font=('arial', 12, 'bold'), 
          fg='grey', 
          bg=white_color)
        lab_product_unit_price.grid(row=3, column=0, sticky='w')
        entry_product_unit_price = Entry(booking_fields, 
          bg='white', 
          width=20, 
          font=('arial',12, 'bold'), 
          bd=2, 
          textvariable=product_unit_price)
        entry_product_unit_price.grid(row=3, column=1) 

        # product_quantity
        lab_product_quantity = Label(booking_fields, 
          text='Quantity: ', 
          padx=2, 
          pady=2, 
          font=('arial', 12, 'bold'), 
          fg='grey', 
          bg=white_color)
        lab_product_quantity.grid(row=4, column=0,sticky='w')
        entry_product_quantity = Entry(booking_fields, 
          bg='white', 
          width=20, 
          font=('arial',12, 'bold'), 
          bd=2,
          textvariable=product_quantity)
        entry_product_quantity.grid(row=4, column=1) 

        # product_total_price
        lab_product_total_price = Label(booking_fields, 
          text='Total Price ($): ', 
          padx=2, 
          pady=2, 
          font=('arial', 12, 'bold'), 
          fg='grey', 
          bg=white_color)
        lab_product_total_price.grid(row=5, column=0, sticky='w')
        entry_product_total_price = Entry(booking_fields, 
          bg='white', 
          width=20, 
          font=('arial',12, 'bold'), 
          bd=2,
          textvariable=product_total_price)
        entry_product_total_price.grid(row=5, column=1)  

        # created_on

        today = date.today()
        date_format = today.strftime("%B %d, %Y")

        created_on.set(date_format)

        lab_created_on = Label(booking_fields, 
          text='Date (dd/mm/yyyy): ', 
          padx=2, 
          pady=2, 
          font=('arial', 12, 'bold'), 
          fg='grey', 
          bg=white_color)
        lab_created_on.grid(row=6, column=0, sticky='w')
        entry_created_on = Entry(booking_fields, 
          bg='white', 
          width=20, 
          font=('arial',12, 'bold'), 
          bd=2, 
          state='readonly',
          textvariable=created_on)
        entry_created_on.grid(row=6, column=1) 


        # btn frame
        btn_frame = Frame(booking_fields, padx=5, pady=4, relief='flat', bg=white_color)
        btn_frame.grid(row=7, column=0, columnspan=2, pady=10)

        # total btn
        total_btn = Button(btn_frame, 
          text='Total', 
          bg='#076',
          fg='white', 
          width=6, 
          height=1,
          relief='flat',
          font=('arial',12), 
          bd=2, 
          activeforeground='white',
          activebackground='#4b8598',
          command=get_total_cost_data)
        total_btn.grid(row=0, column=0, pady=5, padx=1)   

        # add btn
        add_btn = Button(btn_frame, 
          text='Add', 
          bg='gray',
          fg='white', 
          relief='flat',
          width=6, 
          height=1,
          activeforeground='white',
          activebackground='#4b8598',
          font=('arial',12), 
          bd=2, 
          command=add_product_data)
        add_btn.grid(row=0, column=1, pady=5, padx=1)

        # update btn
        update_btn = Button(btn_frame, 
          text='Update', 
          bg='gray',
          fg='white', 
          width=6, 
          height=1,
          relief='flat',
          activeforeground='white',
          activebackground='#4b8598',
          font=('arial',12), 
          bd=2, 
          command=update_product_data)
        update_btn.grid(row=0, column=2, pady=5, padx=1)

        # clear btn
        clear_btn = Button(btn_frame, 
          text='Clear', 
          bg='gray', 
          fg='white',
          relief='flat',
          width=6, 
          height=1,
          activeforeground='white',
          activebackground='#4b8598',
          font=('arial',12), 
          bd=2, 
          command=clearAll)
        clear_btn.grid(row=0, column=3, pady=5, padx=1)   


        # delete btn
        delete_btn = Button(btn_frame, 
          text='Delete', 
          bg='red', 
          fg='white',
          width=6, 
          height=1,
          relief='flat',
          activeforeground='white',
          activebackground='#4b8598', 
          font=('arial',12), 
          bd=2, 
          command=delete_product_data)
        delete_btn.grid(row=0, column=4, pady=5, padx=1)       

        # search btn
        search_btn = Button(btn_frame, 
          text='Search', 
          bg='#4b8598', 
          fg='white',
          width=6, 
          relief='flat',
          height=1, 
          font=('arial',12), 
          bd=2, 
          activeforeground='white',
          activebackground='#72404d',
          command=search_product_data)
        search_btn.grid(row=0, column=5, pady=5, padx=1)





 



def close_app(event):
    root.quit()
    exit()


HomePageView(root)

root.bind('<Escape>', close_app)

root.mainloop()



# pyinstaller --onefile -w -i logo.ico --add-data "db.py;." app.py






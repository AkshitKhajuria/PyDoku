import tkinter as tk
from time import sleep

class Sudoku:
    def __init__(self, master):
        self.grid = {}
        self.e = None
        self.canvas_width = 300
        self.canvas_height = 300
        
        self.canvas = tk.Canvas(master,bg="#fafafa", width=self.canvas_width, height=self.canvas_height)
        self.t = tk.Entry(self.canvas)
        self.t.bind("<KeyRelease>",self.keyPressed)
        self.canvas.pack()
        self.canvas.bind("<Button 1>",self.click)

        self.cell_width = self.canvas_width/9
        self.cell_height = self.canvas_height/9

        for x in range(1,9):
            width=1
            fill="#4f4f4f"
            if(x%3==0):
                width=2
                fill="#000000"
            else:
                width=1
                fill="#4f4f4f"
            self.canvas.create_line(self.cell_width*x, 0, self.cell_width*x, self.canvas_height, width=width, fill=fill)

        for y in range(1,9):
            width=1
            fill="#4f4f4f"
            if(y%3==0):
                width=2
                fill="#000000"
            else:
                width=1
                fill="#4f4f4f"
            self.canvas.create_line(0, self.cell_height*y, self.canvas_width, self.cell_height*y, width=width, fill=fill)
    
    def click(self, eventorigin):
        x = eventorigin.x
        y = eventorigin.y
        rect_x = int(x/self.cell_width)*self.cell_width
        rect_y = int(y/self.cell_height)*self.cell_height
        coords = [rect_x,rect_y,rect_x+self.cell_width,rect_y,rect_x+self.cell_width,rect_y+self.cell_height,rect_x,rect_y+self.cell_height]
        # For some stupid reason, this line below didn't work as expected. So I had to choose the hard way.
        # h_box = self.canvas.create_rectangle(rect_x, rect_y, self.cell_width, self.cell_height, outline="#15fa00", width=3)

        editable = self.getCell(x/self.cell_width,y/self.cell_height)[1]
        if editable:
            #Show a green box highlight and edit
            h_box = self.canvas.create_polygon(coords, outline="#15fa00", fill='', width=3)
            self.edit(rect_x, rect_y)
        else:
            #Show a red box highlight
            h_box = self.canvas.create_polygon(coords, outline="#d61111", fill='', width=3)
        self.canvas.after(200,lambda : self.canvas.delete(h_box))

    def edit(self,cordx:int,cordy:int):
        if self.e is None:
            pass
        else:
            self.canvas.delete(self.e)
            
        self.e = self.canvas.create_window(cordx+1,cordy+1,window=self.t,width=self.cell_width-1,height=self.cell_height-1,anchor=tk.NW)
        self.t.delete(0,tk.END)
        self.t.focus_set()
        
    def keyPressed(self, event):
        val = self.t.get().strip()
        try:
            val = int(val)
        except ValueError:
            print("Not a number!")
        else:
            x,y = (self.t.winfo_x()+1)/self.cell_width,(self.t.winfo_y()+1)/self.cell_height
            self.updateCell(x,y,val)

    def updateCell(self,x,y,value):
        if value<=9:
            t = self.getCell(x,y)
            if t[1]:
                #If it's an editable cell
                t[0] = value
                self.canvas.itemconfigure(t[-1],text=value)
                self.grid[(x,y)] = t

    def getCell(self, x:int, y:int):
        val = self.grid[(int(x),int(y))]
        return val

    def populate(self, X:[[]]):
        c = self.canvas
        '''Dict->(X,Y) : [value,True/Flase,id]
                   ^        ^        ^     ^
              X,Y coords  value  editable  object id'''
        for i in range(9):
            for j in range(9):
                text_x = j*self.cell_width+self.cell_width/2
                text_y = i*self.cell_height+self.cell_height/2
                val = X[i][j]
                if val == ' ':
                    t = c.create_text(text_x,text_y,text=val,font=('Times', '14'))
                    self.grid[(j,i)] = [ val, True, t]
                else:
                    t = c.create_text(text_x,text_y,text=val,font=('bold'))
                    self.grid[(j,i)] = [ val, False, t]
    


####################################
master = tk.Tk()
master.resizable(False, False)
game=Sudoku(master)
ex= [  
    [' ',' ',' ',  ' ',' ',' ',   2 ,' ',' '],
    [' ', 8 ,' ',  ' ',' ', 7 ,  ' ', 9 ,' '],
    [ 6 ,' ', 2 ,  ' ',' ',' ',   5 ,' ',' '],
    [' ', 7 ,' ',  ' ', 6 ,' ',  ' ',' ',' '],
    [' ',' ',' ',   9 ,' ', 1 ,  ' ',' ',' '],
    [' ',' ',' ',  ' ', 2 ,' ',  ' ', 4 ,' '],
    [' ',' ', 5 ,  ' ',' ',' ',   6 ,' ', 3 ],
    [' ', 9 ,' ',   4 ,' ',' ',  ' ', 7 ,' '],
    [' ',' ', 6 ,  ' ',' ',' ',  ' ',' ',' ']
    ]
game.populate(ex)

tk.mainloop()

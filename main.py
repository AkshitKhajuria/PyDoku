import tkinter as tk
from tkinter import font
from time import sleep

class Sudoku:
    #Canvas background
    canvas_bg = "#fafafa" #impure white
    #Grid lines
    line_normal = "#4f4f4f" #dark grey
    line_thick = "#000000" #pure black
    #cell highlight box
    hbox_green = "#15fa00" #light green
    hbox_red = "#d61111" #red

    def __init__(self, master):
        self.grid = {}
        self.e = None
        self.canvas_width = 300
        self.canvas_height = 300
        #The sudoku grid
        self.canvas = tk.Canvas(master,bg=self.canvas_bg, width=self.canvas_width, height=self.canvas_height)
        self.t = tk.Entry(self.canvas)
        self.t.bind("<KeyRelease>",self.keyPressed)
        self.canvas.grid(columnspan=2)
        self.canvas.bind("<Button 1>",self.click)
        #Solve button
        self.btn_solve = tk.Button(master,text='Solve', width=8)
        self.btn_solve.grid(row=1, padx=5, pady=5)
        #Generate button
        self.btn_gen = tk.Button(master,text='Generate', width=8)
        self.btn_gen.grid(row=1, column=1, padx=5, pady=5)
        #Individual cell width and height
        self.cell_width = self.canvas_width/9
        self.cell_height = self.canvas_height/9
        #Draw vertical lines
        for x in range(1,9):
            width=1
            fill=self.line_normal
            if(x%3==0):
                #Draw thicker black lines for seperating 3x3 boxes
                width=2
                fill=self.line_thick
            else:
                #Draw normal thin dark-grey lines
                width=1
                fill=self.line_normal
            self.canvas.create_line(self.cell_width*x, 0, self.cell_width*x, self.canvas_height, width=width, fill=fill)
        #Draw horizontal lines in the same way
        for y in range(1,9):
            width=1
            fill=self.line_normal
            if(y%3==0):
                width=2
                fill=self.line_thick
            else:
                width=1
                fill=self.line_normal
            self.canvas.create_line(0, self.cell_height*y, self.canvas_width, self.cell_height*y, width=width, fill=fill)
    
    def click(self, eventorigin):
        x = eventorigin.x
        y = eventorigin.y
        #Calcilate top-left x,y coords of cell clicked by mouse
        rect_x = int(x/self.cell_width)*self.cell_width
        rect_y = int(y/self.cell_height)*self.cell_height
        #Coords for drawing a square to highlight clicked cell
        coords = [rect_x,rect_y,rect_x+self.cell_width,rect_y,rect_x+self.cell_width,rect_y+self.cell_height,rect_x,rect_y+self.cell_height]
        # For some stupid reason, this line below didn't work as expected. So I had to choose the hard way.
        # h_box = self.canvas.create_rectangle(rect_x, rect_y, self.cell_width, self.cell_height, outline="#15fa00", width=3)
        #Get cell info
        editable = self.getCell(x/self.cell_width,y/self.cell_height)[1]
        if editable:
            #It's a cell you can edit
            #Show a green box highlight and edit
            h_box = self.canvas.create_polygon(coords, outline=self.hbox_green, fill='', width=3)
            self.edit(rect_x, rect_y)
        else:
            #It's a cell containing a clue number, cannot edit
            #Show a red box highlight
            h_box = self.canvas.create_polygon(coords, outline=self.hbox_red, fill='', width=3)
        self.canvas.after(200,lambda : self.canvas.delete(h_box))

    def edit(self,cordx:int,cordy:int):
        #Create a entry inside a small canvas window
        #make sure it's actuall initilized before deleting it
        if self.e is None:
            #Not initilized, else block skipped
            pass
        else:
            #Canvas window initilized, delete and reset it to current position
            self.canvas.delete(self.e)
        #Create a mini edit window that just fits the cell    
        self.e = self.canvas.create_window(cordx+1,cordy+1,window=self.t,width=self.cell_width-1,height=self.cell_height-2,anchor=tk.NW)
        #Clean up
        self.t.delete(0,tk.END)
        self.t.focus_set()
        
    def keyPressed(self, event):
        val = self.t.get().strip()
        try:
            #If input is a number between 1-9, this won't raise any errors
            val = int(val)
            if(val>9 or val<1):
                raise ValueError
        except ValueError:
            print("Invalid input!")
            self.t.delete(0,tk.END)
        else:
            #Get x,y coords of edit window and calculate cell row,column values
            x,y = (self.t.winfo_x()+1)/self.cell_width,(self.t.winfo_y()+1)/self.cell_height
            #Update cell with new value
            self.updateCell(x,y,val)
            self.canvas.delete(self.e)

    def updateCell(self,x,y,value):
        #Get cell information stored in dict self.grid
        t = self.getCell(x,y)
        t[0] = value
        #Update display value by using item id
        self.canvas.itemconfigure(t[2],text=value)
        #Update the dict
        self.grid[(x,y)] = t

    def getCell(self, x:int, y:int):
        #Returns info of cell at 'x' row 'y' column
        val = self.grid[(int(x),int(y))]
        return val

    def populate(self, X:[[]]):
        #Populates the sudoku grid with given 9x9 matrix and also store it in a dict
        c = self.canvas
        #The bookeeping is managed as shown below
        '''Dict->(X,Y) : [value,True/Flase,id]
                   ^        ^        ^     ^
              X,Y coords  value  editable  object id'''
        for i in range(9):
            for j in range(9):
                #Calculate x,y position of center of cell
                text_x = j*self.cell_width+self.cell_width/2
                text_y = i*self.cell_height+self.cell_height/2
                val = X[i][j]
                if val == ' ':
                    t = c.create_text(text_x,text_y,text=val,font=('Times', '14'))
                    self.grid[(j,i)] = [ val, True, t]
                else:
                    t = c.create_text(text_x,text_y,text=val,font=('bold'))
                    self.grid[(j,i)] = [ val, False, t]

    def Solve(self):
        pass

  
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

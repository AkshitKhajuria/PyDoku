import tkinter as tk
from tkinter import font
from time import sleep

count = 0

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
        self.btn_solve = tk.Button(master,text='Solve', command=self.solve, width=8)
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
            x,y = (self.t.winfo_x())/self.cell_width,(self.t.winfo_y())/self.cell_height
            #Update cell with new value
            self.updateCell(val,x,y)
            self.canvas.delete(self.e)

    def updateCell(self,value,x,y,editable=True):
        #Get cell information stored in dict self.grid
        t = self.getCell(x,y)
        #Update values
        t[0] = value
        t[1] = editable
        text=value
        if value==0:
            text=' '
        #Update display value by using item id
        self.canvas.itemconfigure(t[2],text=text)
        self.canvas.update()
        #Update the dict
        self.grid[(x,y)] = t

    def getCell(self, x:int, y:int):
        #Returns info of cell at 'x' row 'y' column
        x=int(x)
        y=int(y)
        val = self.grid[(x,y)]
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
                if val == 0:
                    t = c.create_text(text_x,text_y,text=' ',font=('Times', '14'))
                    self.grid[(j,i)] = [ val, True, t]
                else:
                    t = c.create_text(text_x,text_y,text=val,font=('bold'))
                    self.grid[(j,i)] = [ val, False, t]

    def getValue(self, row:int, col:int):
        #Return value at row, column
        return self.grid[(row,col)][0]

    def printGrid(self):
        #Utility function to print the grid
        for i in range(9):
            x=[]
            for j in range(9):
                x.append(self.getValue(j,i))
            print(x)

    def solve(self):
        #Start by finding an empty cell
        x,y = self.findEmpty()
        #If no cells are empty, our job is done
        if (x,y)==(None,None):
            #Print the no. of times solve() was called
            # print(count, "Iterations")
            return True
        
        #Keep a track of the number of function calls
        global count
        count+=1
        
        #Try putting in numbers from 1-9
        for i in range(1,10):
            #Check if number will satisfy sub-grid rule and row-column rule
            if self.is_SubGrid_Safe(i,x,y) and self.is_Cell_Safe(i,x,y):
                #Yes, then update the cell
                self.updateCell(i,x,y,False)
                # self.canvas.after(10,self.updateCell(i,x,y))
                #Now repeat for remaining cells
                nxt = self.solve()
                if nxt==False:
                    #The value chose earlier is wrong, so backtrack
                    self.updateCell(0,x,y,True)
                else:
                    #All went well, so return true
                    return True
        #Cannot find any number, so return false (backtrack)
        return False
    
    def findEmpty(self):
        #Utility function to find an empty cell
        for i in range(9):
            for j in range(9):
                cell_val = self.getCell(i,j)[1]
                if cell_val:
                    return (i,j)
        return (None,None)

    def is_SubGrid_Safe(self,val,x,y)->bool:
        #Checks if the sub-grid rule is satisfied for the number 'val' at given row 'x',column 'y'
        #Figure out the sub grid x,y
        sgrid_x = int(x/3)*3
        sgrid_y = int(y/3)*3
        #Search the sub-grid
        for i in range(sgrid_x,sgrid_x+3):
            for j in range(sgrid_y,sgrid_y+3):
                if val==self.getValue(i,j):
                    #This number already exists, rule violated
                    return False
        #No duplicate number found in sub-grid, rule intact
        return True

    def is_Cell_Safe(self,val,x,y)->bool:
        #Check if the number 'val' already exists in the row 'x' or column 'y'
        for i in range(9):
            if val==self.getValue(x,i):
                return False
            if val==self.getValue(i,y):
                return False
        #Row-column rule intact
        return True
       
  
####################################
master = tk.Tk()
master.resizable(False, False)
game=Sudoku(master)
ex= [   
    [3, 0, 6, 5, 0, 8, 4, 0, 0], 
    [5, 2, 0, 0, 0, 0, 0, 0, 0], 
    [0, 8, 7, 0, 0, 0, 0, 3, 1], 
    [0, 0, 3, 0, 1, 0, 0, 8, 0], 
    [9, 0, 0, 8, 6, 3, 0, 0, 5], 
    [0, 5, 0, 0, 9, 0, 6, 0, 0], 
    [1, 3, 0, 0, 0, 0, 2, 5, 0], 
    [0, 0, 0, 0, 0, 0, 0, 7, 4], 
    [0, 0, 5, 2, 0, 6, 3, 0, 0]
    ]  
game.populate(ex)
tk.mainloop()

from tkinter import *
from time import sleep

class Sudoku:
    def __init__(self, master):
        self.canvas_width = 300
        self.canvas_height = 300
        
        self.canvas = Canvas(master, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()
        self.canvas.bind("<Button 1>",self.paint)

        self.cell_width = self.canvas_width/9
        self.cell_height = self.canvas_height/9

        for x in range(1,9):
            width=1
            if(x%3==0):
                width=2
            else:
                width=1
            self.canvas.create_line(self.cell_width*x, 0, self.cell_width*x, self.canvas_height, width=width)

        for y in range(1,9):
            width=1
            if(y%3==0):
                width=2
            else:
                width=1
            self.canvas.create_line(0, self.cell_height*y, self.canvas_width, self.cell_height*y, width=width)
    
    def paint(self, eventorigin):
        x = eventorigin.x
        y = eventorigin.y
        rect_x = int(x/self.cell_width)*self.cell_width
        rect_y = int(y/self.cell_height)*self.cell_height
        coords = [rect_x,rect_y,rect_x+self.cell_width,rect_y,rect_x+self.cell_width,rect_y+self.cell_height,rect_x,rect_y+self.cell_height]
        # For some stupid reason, this line below didn't work as expected. So I had to choose the hard way.
        # self.canvas.create_rectangle(rect_x, rect_y, self.cell_width, self.cell_height, outline="#15fa00", width=3)
        poly_id = self.canvas.create_polygon(coords, outline="#15fa00", fill='', width=3)
        self.canvas.after(200,lambda : self.canvas.delete(poly_id))
        

    def populate(self, X : []):
        pass

master = Tk()
master.resizable(False, False)
Sudoku(master)

mainloop()
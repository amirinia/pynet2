# Author: amirinia


from tkinter import *
import numpy as np

size_of_board = 1000
symbol_size = (size_of_board / 150 ) 
symbol_thickness = 15

symbol_O_color = 'green'



class Network():
    # ------------------------------------------------------------------
    # Initialization Functions:
    # ------------------------------------------------------------------
    def __init__(self):
        self.window = Tk()
        self.window.title('Network Maker')
        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board)
        self.canvas.pack()
        # Input from user in form of clicks
        self.window.bind('<Button-1>', self.click)
        self.pos = []
        self.board_status = np.zeros(shape=(300, 300))

        #self.button1 = Button(self.canvas, text='quit', command=quit)
        #self.button1.pack()
        self.buttonB = self.canvas.create_rectangle(0, 0, 100, 60, fill="white", outline="black")
        self.buttonTXT = self.canvas.create_text(50, 30, text="Close")
        self.canvas.tag_bind(self.buttonB, "<Button-1>",func=self.mexit)

    def mexit(self,buttonB):
        print("Positions are saved")
        print((self.pos))
        with open("pos.txt", "w") as file:
            file.write(str(self.pos))
        self.makeinitialnetwork(self.pos)
        exit()
    
    def mainloop(self):
        self.window.mainloop()


    # ------------------------------------------------------------------
    # Drawing Functions:
    # ------------------------------------------------------------------

    def draw_node(self, logical_position):
        logical_position = np.array(logical_position)
        # logical_position = grid value on the board
        # grid_position = actual pixel values of the center of the grid
        grid_position = self.convert_logical_to_grid_position(logical_position)
        if(grid_position[0] >100 or grid_position[1]>60):
            self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                    grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                    outline=symbol_O_color)
            print((logical_position.tolist())) #<class 'numpy.ndarray'>
            self.pos.append(logical_position.tolist())
            if(str(logical_position) == "[0 0]"):
                print("it is done")

                self.window.quit()


    
        
    # ------------------------------------------------------------------
    # Logical Functions:
    # ------------------------------------------------------------------

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (size_of_board / 300) * logical_position + size_of_board / 60

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (size_of_board / 300), dtype=int)

    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True

            #print("status ",self.board_status[0][0])


    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

                  
        if not self.is_grid_occupied(logical_position):
                    self.draw_node(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1


import simpy
import network 
import node
import message
import time
import gui
import config


env = simpy.Environment()



    def makeinitialnetwork(self,positions):
        for i in positions:
            print(i[0],i[1])
        pass

instance = Network()
instance.mainloop()
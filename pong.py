import tkinter as tk


# inherits from object as the seeing we will pass a range of canvas items
# accepts a canvas object and also an item object
class GameObject(object):
    def __init__(self, canvas, item):
        # initializes the instance with and canvas and item
        self.canvas = canvas
        self.item = item

    # Returns the coordinates of the bounding box of an item
    def get_position(self):
        return self.canvas.coords(self.item)

    # Moves an item by a horizontal and a vertical offset.
    def move(self, x, y):
        self.canvas.move(self.item, x, y)

    # Deletes an item from the canvas.
    def delete(self):
        self.canvas.delete(self.item)


class Ball(GameObject):
    def __init__(self, canvas, x, y):
        # sets the radius, the initial the direction of the ball from the paddle and the speed
        self.radius = 10
        self.direction = [1, -1]
        self.speed = 10
        # creates the ball on the canvas
        item = canvas.create_oval(x - self.radius, y - self.radius,
                                  x + self.radius, y + self.radius,
                                  fill='white')
        super(Ball, self).__init__(canvas, item)


class Paddle(GameObject):
    def __init__(self, canvas, x, y):
        #set the height and width
        self.width = 80
        self.height = 10
        self.ball = None
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill='blue')
        super(Paddle, self).__init__(canvas, item)

    def set_ball(self, ball):
        self.ball = ball

    #the move method is responsible movement of the paddle
    def move(self, offset):
        #gets the current position
        coords = self.get_position()
        #retrieves the canvas width
        width = self.canvas.winfo_width()
        #if both and minimum x-axis coordinates, plys the offset produced by the movement
        #are inside the boundaries of the canvas
        if coords[0] + offset >= 0 and coords[2] + offset <= width:
            #move the underlying item
            super(Paddle, self).move(offset, 0)
            #if the paddle still has a reference to the ball (this happens when the game has not been started)
            if self.ball is not None:
                self.ball.move(offset, 0)

#draws a rectangle similar to the paddle class
class Brick(GameObject):
    COLORS = {1: '#999999', 2: '#555555', 3: '#222222'}

    def __init__(self, canvas, x, y, hits):
        self.width = 75
        self.height = 20
        self.hits = hits
        #The class variable called COLORS is a dictionary—a data structure that contains key / value pairs with
        #the number of hits that the brick has left, and the corresponding color.
        color = Brick.COLORS[hits]
        # With this tag, we can check whether the game is over when the number of remaining items with this tag is zero
        item = canvas.create_rectangle(x - self.width / 2,
                                       y - self.height / 2,
                                       x + self.width / 2,
                                       y + self.height / 2,
                                       fill=color, tags='brick')
        super(Brick, self).__init__(canvas, item)


    def hit(self):
        # the number of hits of the brick instance is decreased by 1
        self.hits -= 1
        if self.hits == 0:
            #if the number of hits remaining is 0, delete the brick from the canvas
            self.delete()
        else:
            #change the color of the brick
            self.canvas.itemconfig(self.item,
                                   fill=Brick.COLORS[self.hits])

class Game(tk.Frame):
    def __init__(self, master):
        # initializes the Frame object
        # parent object is a frame
        # http://effbot.org/tkinterbook/frame.htm
        super(Game, self).__init__(master)
        # create instance variables to hold lives, width and height of the window
        self.lives = 3
        self.width = 610
        self.height = 400
        # create a new canvas
        # http://effbot.org/tkinterbook/canvas.htm
        self.canvas = tk.Canvas(self, bg='#aaaaff',
                                width=self.width,
                                height=self.height)
        # draw the canvas
        # draw the root window
        self.canvas.pack()
        self.pack()

        # creates a green rectangle
        #item = self.canvas.create_rectangle(10,10,100,80, fill='green')
        # use the game object class
        #game_object = GameObject(self.canvas,item) #create new instance
        #print(game_object.get_position())
        # game_object.move(20, 100)

        # creates a ball
        #item = Ball(self.canvas, 20, 50)
        #game_object = GameObject(self.canvas,item)

        # creates the paddle
        #item = Paddle(self.canvas, 20, 50)
        #game_object = GameObject(self.canvas,item)
        #print(game_object.get_position())

        #creates the brick class
        #item = Brick(self.canvas,100,50,1)
        #game_object = GameObject(self.canvas,item)
        #print(game_object.get_position())

        #their insertion into the self.items dictionary.
        #This attribute contains all the canvas items that can
        #collide with the ball, so we add only the bricks and the player's paddle to it.
        self.items = {}
        self.ball = None
        self.paddle = Paddle(self.canvas, self.width / 2, 326)
        self.items[self.paddle.item] = self.paddle
        for x in range(5, self.width - 5, 75):
            print(x)
            self.add_brick(x + 37.5, 50, 2)
            self.add_brick(x + 37.5, 70, 1)
            self.add_brick(x + 37.5, 90, 1)

        ##########################################################

        self.hud = None
        self.setup_game()
        #sets the focus on the canvas, so the input events are directly bound to this widget
        self.canvas.focus_set()
        #Then we can bind the left and right keys to paddle's move() method and the spacebar to trigger
        #the game start
        self.canvas.bind('<Left>',
                         lambda _: self.paddle.move(-10))
        self.canvas.bind('<Right>',
                        lambda _: self.paddle.move(10))

    def setup_game(self):
        self.add_ball()
        self.update_lives_text()
        self.text = self.draw_text(300, 200,
                                   'Press Space to start')
        self.canvas.bind('<space>', lambda _: self.start_game())

    def add_brick(self, x, y, hits):
        brick = Brick(self.canvas, x, y, hits)
        self.items[brick.item] = brick

    def add_ball(self):
        if self.ball is not None:
            self.ball.delete()
        paddle_coords = self.paddle.get_position()
        x = (paddle_coords[0] + paddle_coords[2]) * 0.5
        self.ball = Ball(self.canvas, x, 310)
        self.paddle.set_ball(self.ball)

    def draw_text(self, x, y, text, size='40'):
        font = ('Helvetica', size)
        return self.canvas.create_text(x, y, text=text,
                                       font=font)
    def update_lives_text(self):
        text = 'Lives: %s' % self.lives
        if self.hud is None:
            self.hud = self.draw_text(50, 20, text, 15)
        else:
            self.canvas.itemconfig(self.hud, text=text)

    def start_game(self):
        pass

if __name__ == '__main__':
    # creates new instance of tk and creates a new window
    # sets the title of the window
    root = tk.Tk()
    root.title('Hello, Pong!')
    # our new type called Game inherits from Frame
    game = Game(root)
    # load the window and listen for GUI objects
    game.mainloop()

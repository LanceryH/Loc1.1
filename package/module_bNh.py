from copy import deepcopy
import numpy as np

class node:
    """
    A class for a node within the quadtree.
    
    We use the terminology "child" for nodes in the next depth level - consistent with tree nomenclature
    If a node is "childless" then it represents a body
    """
    def __init__(self, x, y, px, py, m):
        """
        Initializes a childless node
        
        m - Mass of node
        x - x-coordinate centre of mass
        y - y-coordinate centre of mass
        px - x- coordinate of momentum
        py - y-coordinate of momentum
        pos - centre of mass array
        mom - momentum array
        child - child node
        s - side-length (depth=0 s=1)
        relpos = relative position
        """
        self.m = m
        self.pos = np.array([x,y])
        self.mom = np.array([px,py])
        self.child = None
        
    def next_quad(self):
        """
        Places node in next quadrant and returns quadrant number
        """
        self.s = 0.5*self.s
        return self.divide_quad(1) + 2*self.divide_quad(0)
    
    def divide_quad(self, i):
        """
        Places node in next level quadrant and recomputes relative position
        """
        self.relpos[i] *= 2.0
        if self.relpos[i] < 1.0:
            quadrant = 0
        else:
            quadrant = 1
            self.relpos[i] -= 1.0
        return quadrant
    
    def reset_quad(self):
        """
        Repositions to the zeroth depth quadrant (full space)
        """
        self.s = 1.0
        self.relpos = self.pos.copy()
        
        
    def dist(self, other):
        """
        Calculates distance between node and another node
        """
        return np.linalg.norm(self.pos - other.pos)
    
    def force_ap(self, other):
        """
        Force applied from current node to other
        """
        d = self.dist(other)
        return (self.pos - other.pos) * (self.m * other.m / d**3)
    

def add_body(body, node):
    """
    Adds body to a node of quadtree. A minimum quadrant size is imposed
    to limit the recursion depth.
    """
    new_node = body if node is None else None
    min_quad_size = 1.e-5
    if node is not None and node.s > min_quad_size:
        if node.child is None:
            new_node = deepcopy(node)
            new_node.child = [None for i in range(4)]
            quad = node.next_quad()
            new_node.child[quad] = node
        else:
            new_node = node

        new_node.m += body.m
        new_node.pos += body.pos
        quad = body.next_quad()
        new_node.child[quad] = add_body(body, new_node.child[quad])
    return new_node

def force_on(body, node, theta):
    if node.child is None:
        return node.force_ap(body)
    
    if node.s < node.dist(body) * theta:
        return node.force_ap(body)
    return sum(force_on(body, c, theta) for c in node.child if c is not None)

def verlet(bodies, root, theta, G, dt):
    for body in bodies:
        force = G * force_on(body, root, theta)
        body.mom += dt * force
        body.pos += dt * body.mom / body.m

       
def Rk4(bodies,dt,M):
    y=[]
    for body in bodies:
        y.append((body.mom)[0])
        y.append((body.mom)[1])
        y.append(0)
        y.append((body.pos)[0])
        y.append((body.pos)[1])
        y.append(0)
    y=np.reshape(y,(60,1))
    h=dt
    t=0
    k1=h*f(t,y,M)
    k2=h*f(t+h/2, y+k1/2,M)
    k3=h*f(t+h/2, y+k2/2,M)
    k4=h*f(t+h, y+k3,M)
    y=y+(1/6)*(k1 +2*k2 +2*k3 + k4)
    t+=h    
    return(y)   

def model_step(bodies, theta, g, step):
    root = None
    for body in bodies:
        body.reset_quad()
        root = add_body(body, root)
    verlet(bodies, root, theta, g, step)

########## Main Code ##########
# Parameters
Theta = 0.7
G = 1.e-6
dt = 1.e-2
N_bodies = 10
N_steps = 10

# Fix Seed for Initialization
np.random.seed(123)

# Initial Conditions
Masses = np.random.random(N_bodies)*10
X0 = np.random.random(N_bodies)
Y0 = np.random.random(N_bodies)
PX0 = np.random.random(N_bodies) - 0.5
PY0 = np.random.random(N_bodies) - 0.5

# Initialize
Bodies = [node(x0, y0, pX0, pY0, masses) for (x0, y0, pX0, pY0, masses) in zip(X0, Y0, PX0, PY0, Masses)]
import matplotlib.pyplot as plt
from tqdm import tqdm
# Main Model Loop
def Model_Loop_BH(n):
    plt.figure()
    for i in tqdm(range(n)):
        model_step(Bodies, Theta, G, dt) 
        y=[]
        for body in Bodies:
            y.append((body.mom)[0])
            y.append((body.mom)[1])
            y.append(0)
            y.append((body.pos)[0])
            y.append((body.pos)[1])
            y.append(0)
        y=np.reshape(y,(1,60))[0]
        for j in range(0,N_bodies):
            plt.scatter(y[j*3:((j+1)*3)][0],y[j*3:((j+1)*3)][1])
    plt.show()
Model_Loop_BH(N_steps)

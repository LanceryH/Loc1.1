import tkinter as tk
from tkinter import ttk
import numpy as np
from .module_reso import Resolution
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


color_1="#E0E0EE"
color_2="#FFFFFF"
Pos = ""
class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        notebook = ttk.Notebook(parent)
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TNotebook", background=color_2, borderwidth=0)
        notebook.add(Typ1(notebook), text='Home')
        notebook.add(Typ2(notebook), text='Display')
        notebook.pack()
    
class Typ1(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        
        frame_tab1_left=tk.LabelFrame(self, text="Sandbox", labelanchor="n", padx=5, pady=5)
        frame_tab1_left.grid(row=0,column=0,padx=5,pady=5,rowspan=2)
        global Valuex
        global Valuey
        global teta_list
        Valuex=[]
        Valuey=[]
        teta_list=[]
        def actionclicsouris(event):
            canvas_tab1.focus_set()
            x=event.x
            y=event.y
            if (np.size(Valuex)%2==0):
                global xrouge
                global yrouge
                xrouge=x
                yrouge=y
                canvas_tab1.create_oval(x-3,y-3,x+3,y+3,fill="red")
            else:
                xbleu=x
                ybleu=y
                canvas_tab1.create_oval(x-3,y-3,x+3,y+3,fill="blue")
                canvas_tab1.create_line(x,y,Valuex[-1],-(Valuey[-1]-400),fill="blue",width=1)
            Valuex.append(x)
            Valuey.append(400-y)
            label_pos_x.insert(0, "{},".format(x)) 
            label_pos_y.insert(0, "{},".format(400-y)) 
        canvas_tab1 = tk.Canvas(frame_tab1_left,background="white",height=355,width=355)
        canvas_tab1.pack()
        canvas_tab1.bind("<Button-1>",actionclicsouris)
        
        frame_tab1_right=tk.LabelFrame(self, text="Initialisation", labelanchor="n", padx=5, pady=5)
        frame_tab1_right.grid(row=0,column=1,padx=5,pady=5,columnspan=2,sticky="n")
        
        frame_tab1_right_button=tk.LabelFrame(self, padx=5, pady=5)
        frame_tab1_right_button.grid(row=1,column=1,padx=5,pady=5,columnspan=2,sticky="n")
        
        label_ite = tk.Label(frame_tab1_right, text ='iterat° :')
        label_ite.grid(row=0, column=0,pady=5)
        enter_ite = tk.Entry(frame_tab1_right)
        enter_ite.insert(0 , '5000')
        enter_ite.grid(row=0, column=1,pady=5)
        
        label_t_max = tk.Label(frame_tab1_right, text = 't_max :')
        label_t_max.grid(row=1, column=0,pady=5)
        enter_t_max = tk.Entry(frame_tab1_right)
        enter_t_max.insert(0 , '5')
        enter_t_max.grid(row=1, column=1,pady=5)
        
        label_masses = tk.Label(frame_tab1_right, text = 'mass  :')
        label_masses.grid(row=2, column=0,pady=5)
        enter_masses = tk.Entry(frame_tab1_right)
        enter_masses.insert(0 , "auto")
        enter_masses.grid(row=2, column=1,pady=5)
        
        frame_tab1_right_reso=tk.LabelFrame(frame_tab1_right, text="Methods", labelanchor="n", padx=5, pady=5)
        frame_tab1_right_reso.grid(row=3,column=0,padx=5,pady=5,columnspan=2)
        
        frame_tab1_right_opti=tk.LabelFrame(frame_tab1_right, text="Options", labelanchor="n", padx=5, pady=5)
        frame_tab1_right_opti.grid(row=4,column=0,padx=5,pady=5,columnspan=2)
        
        frame_tab1_right_pos=tk.LabelFrame(frame_tab1_right, text="Values", labelanchor="n", padx=5, pady=5)
        frame_tab1_right_pos.grid(row=5,column=0,padx=5,pady=5,columnspan=2)
        
        label_pos_x  = tk.Entry(frame_tab1_right_pos)
        label_pos_x.insert(0 , "")
        label_pos_x.grid(row=0, column=0)
        
        label_pos_y  = tk.Entry(frame_tab1_right_pos)
        label_pos_y.insert(0 , "")
        label_pos_y.grid(row=1, column=0)
        
        var_opti_hub = tk.IntVar()
        check_hub= tk.Checkbutton(frame_tab1_right_opti,text="Rebond ", variable=var_opti_hub)
        check_hub.grid(row=0, column=0)
        
        def show_values():
            state_show_values=var_opti_none.get()
            if state_show_values==1:   
                global text_values
                text_values=canvas_tab1.create_text(Valuex[-1],-(Valuey[-1]-400)-10,text="{},{}".format(Valuex[-1],-(Valuey[-1]-400)),tag="tag_text")
            if state_show_values==0:      
                canvas_tab1.delete(text_values)
                
        var_opti_none = tk.IntVar()
        check_none= tk.Checkbutton(frame_tab1_right_opti,text="Values ", variable=var_opti_none,command=show_values)
        check_none.grid(row=0, column=1)
        

        
        var_RK2 = tk.IntVar()
        check_rk2= tk.Checkbutton(frame_tab1_right_reso,text="rk2", variable=var_RK2)
        check_rk2.grid(row=0, column=0)
        
        var_RK4 = tk.IntVar()
        check_rk4= tk.Checkbutton(frame_tab1_right_reso,text="rk4", variable=var_RK4)
        check_rk4.grid(row=0, column=1)
        
        var_RK45 = tk.IntVar()
        check_rk45= tk.Checkbutton(frame_tab1_right_reso,text="rk45", variable=var_RK45)
        check_rk45.grid(row=0, column=2)
  
        def apply():   
            Vit=np.array([[0,0,0]])
            Pos=np.array([[0,0,0]])
            Valuexstring=[]
            Valueystring=[]
            label_pos_x_get=label_pos_x.get()
            label_pos_y_get=label_pos_y.get()
            valinte_pos_vitx=""            
            for i in label_pos_x_get:
                if (i!=","):
                    valinte_pos_vitx=valinte_pos_vitx+i
                if (i==","):
                    Valuexstring.append(int(valinte_pos_vitx))
                    valinte_pos_vitx=""   
            valinte_pos_vity=""            
            for i in label_pos_y_get:
                if (i!=","):
                    valinte_pos_vity=valinte_pos_vity+i
                if (i==","):
                    Valueystring.append(int(valinte_pos_vity))
                    valinte_pos_vity=""   
                    
            statecheck1=var_RK2.get()
            statecheck2=var_RK4.get()
            statecheck3=var_RK45.get()
            stateMasses=enter_masses.get()
            state_rebond=var_opti_hub.get()
            nb_corps=int(len(Valuexstring)/2)
            for i in range(nb_corps): 
                    Vx=Valuexstring[-(i*2+1)-1]-Valuexstring[-(i*2)-1]
                    Vy=Valueystring[-(i*2+1)-1]-Valueystring[-(i*2)-1]
                    Vit=np.vstack((Vit,np.array([[Vx,Vy,0]])))
                    Pos=np.vstack((Pos,np.array([[Valuexstring[-(i*2+1)-1],Valueystring[-(i*2+1)-1],0]])))
            Vit=Vit[1:,:]  
            Pos=Pos[1:,:]    
            y=np.vstack((Pos,Vit)).reshape(-1,1)
            N=int(enter_ite.get()) 
            t_max=int(enter_t_max.get())
            
            Masses=[]
            if stateMasses=="auto":        
                for i in range(nb_corps):
                    Masses.append(1000) 
            else:
                mass=stateMasses
                mass=mass+","
                valinte=""            
                for i in mass:
                    if (i!=","):
                        valinte=valinte+i
                    if (i==","):
                        Masses.append(int(valinte))
                        valinte=""               
            global Y 
            if (statecheck1==1 and statecheck2==statecheck3==0):
                Y=Resolution(y,t0=0,tf=t_max,N=N,nb_corps=nb_corps,M=Masses,state_rebond=state_rebond,teta_list=teta_list).RK2()
            if (statecheck2==1 and statecheck1==statecheck3==0):
                Y=Resolution(y,t0=0,tf=t_max,N=N,nb_corps=nb_corps,M=Masses,state_rebond=state_rebond,teta_list=teta_list).RK4()
            if (statecheck3==1 and statecheck1==statecheck2==0):
                Y=Resolution(y,t0=0,tf=t_max,N=N,nb_corps=nb_corps,M=Masses,state_rebond=state_rebond,teta_list=teta_list).RK45()
        button_apply = tk.Button(frame_tab1_right_button,text='Apply',command=apply,height= 1, width=9)
        button_apply.grid(row=0, column=0,padx=5,pady=5)
        
        def reset():
            canvas_tab1.delete("all")
            label_pos_x.delete(0,"end") 
            label_pos_y.delete(0,"end") 
            label_pos_x.insert(0, "") 
            label_pos_y.insert(0, "") 
            return  
        button_reset = tk.Button(frame_tab1_right_button,text='Reset',command=reset,height= 1, width=9)
        button_reset.grid(row=0, column=1,padx=5,pady=5)
        
        
class Typ2(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
                   
        frame_tab1_left=tk.LabelFrame(self, text="Graphic", labelanchor="n", padx=5,pady=5)
        frame_tab1_left.grid(row=0,column=0,padx=5,pady=5)
              
        fig = plt.figure(figsize=(5.2, 3.16))       
        def get_value(val):
            fig.clear()
            plt.xlim(0,355)
            plt.ylim(0,355)
            plt.grid()
            plt.xticks([])
            plt.yticks([])
            for j in range(0,int(np.size(Y[:,0])/3)) : 
                i=int(val)
                if i>1000:
                    plt.plot(Y[j*3,i-1000:i], Y[j*3+1,i-1000:i],color="black",linewidth='0.75')    
                else:
                    plt.plot(Y[j*3,:i], Y[j*3+1,:i],color="black",linewidth='0.75')
                plt.scatter(Y[j*3,i-1], Y[j*3+1,i-1],facecolors='none', edgecolors='r',s=20)
                
                canvas_tab2.draw()      
        canvas_tab2 = FigureCanvasTkAgg(fig, master=frame_tab1_left)
        canvas_tab2.draw()
        toolbar = NavigationToolbar2Tk(canvas_tab2, frame_tab1_left)
        toolbar.update()
        canvas_tab2.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        scale_plot = tk.Scale(self, from_=2, to=5000, orient="vertical",length=370,command=get_value,showvalue=0)
        scale_plot.grid(row=0, column=1,sticky="e")
              
        
def run():
    def quit_me():
            root.quit()
            root.destroy()
    root = tk.Tk()
    root.protocol("WM_DELETE_WINDOW", quit_me)
    root.title('Loc1.1')
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()
    
    
import flet as ft
from cafe_status import AppState, IMOJI


@ft.component
def Pay(state:AppState):
    orders=[]
    for order in state.cart:
        for loop in range(int(order["count"])):
            orders.append(IMOJI[order["name"]])


    return ft.Column(


        controls=[
            ft.Text("Here are your orders!", size= 50),
            ft.Text(orders, size=50),
           
            # ft.Image(src="icon.png", width=100, height=100,),
            ft.Text("Enjoy!", size=50),
        ]
)

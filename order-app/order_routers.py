from fastapi import APIRouter, Depends, status, HTTPException
from .models import User, Order
from .schemas import OrderModel, LoginUser,SignUpModel,OrderStatusModel
from .database import Session, engine
from .oauth import get_current_user
from fastapi.encoders import jsonable_encoder

order_router = APIRouter(
    prefix="/orders",
    tags=['orders']
)

session = Session(bind=engine)

@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderModel,current_user: str = Depends(get_current_user)):

    new_order = Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity,

    )
    session.add(new_order)

    session.commit()

    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status
    }

    return jsonable_encoder(response)


@order_router.get('/showall')
async def show_all_order(current_user: str = Depends(get_current_user)):
                   
                showall = session.query(Order).all()
                return showall

@order_router.get('/get/{id}')
async def show_one_order(id:int,current_user: str = Depends(get_current_user)):
        showone = session.query(Order).filter(Order.id == id).first()
        if not showone:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The given id of {id} id not found')
        return showone

@order_router.delete('/delete/{id}')
async def delete(id:int,current_user: str = Depends(get_current_user)):
        delete = session.query(Order).filter(Order.id == id).first()
        if not delete:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The given id of {id} id not found')
        session.delete(delete)
        session.commit()
        return 'done'

@order_router.put('/put/{id}')
async def change_order(id:int,request:OrderModel,current_user: str = Depends(get_current_user)):
    order = session.query(Order).filter(Order.id == id).first()
     

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No order with id {id} found')

    valid_size = [status[0] for status in Order.PIZZA_SIZES]
    if request.pizza_size not in valid_size:
         raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid order status: {request.pizza_size}. Valid statuses are {valid_size}."
        )
    
    order.quantity = request.quantity
    
    order.pizza_size = request.pizza_size
    session.commit()
    session.refresh(order)
    return order



@order_router.patch('/patch')
async def patch_order(id:int,request:OrderStatusModel,current_user: str = Depends(get_current_user)):
    order = session.query(Order).filter(Order.id == id).first()

    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No order with id {id} found')

    valid_statuses = [status[0] for status in Order.ORDER_STATUSES]  
    
    if request.order_status not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid order status: {request.order_status}. Valid statuses are {valid_statuses}."
        )
    
   
    order.order_status = request.order_status
    
    try:
        session.commit()
        session.refresh(order)
    except Exception as e:
        session.rollback()  
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error occurred")

    return order


@order_router.get("/orders")
async def get_orders_for_current_user(
    current_user: User = Depends(get_current_user)  # Get the current user directly
):
    # Access the user's orders directly via the 'orders' relationship
    order_det = current_user.orders
    
    if not order_det:
        raise HTTPException(status_code=404, detail="No orders found for the current user")
    
    # Return the orders as a list of OrderModel
    return [
        OrderModel(
            quantity=order.quantity,
            order_status=order.order_status,
            pizza_size=order.pizza_size
        ) for order in order_det
    ]

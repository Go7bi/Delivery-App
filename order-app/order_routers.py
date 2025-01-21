from fastapi import APIRouter, Depends, status, HTTPException
from .models import User, Order
from .schemas import OrderModel, LoginUser,SignUpModel,OrderStatusModel,OrderRequest
from .database import Session, engine
from .oauth import get_current_user
from fastapi.encoders import jsonable_encoder

order_router = APIRouter(
    prefix="/orders",
    tags=['orders']
)

session = Session(bind=engine)



@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderRequest, current_user: str = Depends(get_current_user)):
    total_price = 0  

  
    for item in order.items:
        if item.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be a positive number greater than 0"
            )
        
     
        pizza_prices = {
            "SMALL": 200.99,
            "MEDIUM": 250.99,
            "LARGE": 350.99,
            "EXTRA-LARGE": 500.99,
        }
        
        pizza_price = pizza_prices.get(item.pizza_size, 200.99)  
        item_total = pizza_price * item.quantity
        total_price += item_total

        
        new_order = Order(
            pizza_size=item.pizza_size,
            quantity=item.quantity,
            address=order.address,
            total=item_total,  
            user_id=current_user.id
        )
        session.add(new_order)
        session.commit()

    
    if total_price != order.total:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Calculated total price does not match the provided total."
        )

    return {"message": "Order placed successfully", "order_id": new_order.id}



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


# @order_router.get("/orders")
# async def get_orders(current_user: str = Depends(get_current_user)):
#     orders = session.query(Order).filter(Order.user_email == current_user).all()  

#     if not orders:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="No orders found for the current user"
#         )

#     return orders

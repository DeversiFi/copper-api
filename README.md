# Deversifi Copper API endpoints

Deversifi provides a number of REST API endpoints to place and cancel orders using delegated funds associated with a Copper account. These endpoints are detailed on this page.

## Authentication

All user account endpoint calls require authentication in the form of a signature included in the request header.

Along with the request payload and standard header elements, the following are required.

```
'Authorization': user_pub_api_key
'X-Timestamp': timestamp_microseconds
'X-Signature': signature for entire request
```

When signing a request, the following format is expected

```
timestamp_microseconds + verb + url_path + body_payload
```

For example, for a GET request

```
1592221815464000GET/balances
```

for a POST request

```
1592221856871000POST/place{"price": 10.0, "amount": 1.0, "symbol": "BTCUSD", "flags": 0, "uid": 1}
```

These request representations should be signed using HMAC SHA256 and the resulting digest hex encoded.

## Place an order

Places an order on a supported market

#### Request

POST /place

Params:
* uid - A user ID (i.e. 1)
* symbol - The name of the symbol of an available market (i.e. BTCUSD)
* price - The decimal order price (i.e. 6000.0)
* amount - The size of the order (i.e. 0.5)
* flags - Flags that can later be used to customize the order type (for now set to 0)

#### Response
```
["/place", "OK", 13043453714433 ]
```

## Cancel an order


#### Request

POST /cancel

Params:
* id - The order ID that uniquely identifies the order to cancel. Is returned by the /place endpoint

#### Response
```
["/cancel", "OK", 13043453714433 ]
```

## All open orders
List all open orders for a user

Possible order states

* Pending place
* Placed
* Partially filled
* Partially filled pending cancel
        case ActiveOrder::OrderStatus::PartiallyFilledPendingCancel:
            return "Partially filled pending cancel";
        case ActiveOrder::OrderStatus::PartiallyFilledCancelled:
            return "Partially filled";
        case ActiveOrder::OrderStatus::Filled:
            return "Filled";
        case ActiveOrder::OrderStatus::PendingCancel:
            return "Pending cancel";
        case ActiveOrder::OrderStatus::Cancelled:
            return "Cancelled";
        case ActiveOrder::OrderStatus::Unknown:

#### Request 

GET /openorders

No parameters

#### Response
```
[
    "/allorders", 
    "OK", 
    [
        ["13043455336449","1592218690474685500","0","0","10.000000","1.000000","0.000000","Placed"],
        ...
    ] 
]
```

TODO list states

## All orders

List all orders, open and historical for a user

#### Request

GET /openorders
No parameters

#### Response

```
[
    "/allorders",
    "OK",
    [
        ["13039943819265","1591790024903972700","0","0","10.000000","1.000000","0.000000","Cancelled"]
        ...
    ] 
]
```

## Get balances

Lists all balances for a particular user

#### Request

GET /balances

No parameters

#### Response

```
[
    "/balances",
    "OK",
    [
        ["BTC",10.000000,0.000000],
        ["USD",1000.000000,10.000000],
        ["LTC",1000.000000,0.000000],
        ["ETH",0.000000,0.000000]
    ]
]
```

Each token's balance follows the pattern

```
[Token, Total Wallet Balance, Reserved Wallet Balance]
```

Reserved wallet balance tracks the value of open orders.  Available wallet balance is thus the difference between Total and Reserved.

## Supported markets

Returns presently supported tokens

#### Request
GET /markets

No parameters

#### Response
```
[
    "/markets",
    "OK",
    [
        "BTC","USD","LTC","ETH"
    ]
]
```
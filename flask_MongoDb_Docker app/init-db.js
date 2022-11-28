db = db.getSiblingDB("DSstore");
db.users.drop();
db.flights.drop();
db.admins.drop();
db.reservations.drop();



  db.admins.insertMany(
    [{
      "_id": {
        "$oid": "632aa4033f6f2a74c70643db"
      },
      "usernameA": "mary",
      "emailA": "mary@gmail.com",
      "passwordA": "AntePali2",
      "status": true
    },{
      "_id": {
        "$oid": "632ad4423a8a3b1ecd67b0fa"
      },
      "emailA": "makro@gmail.com",
      "usernameA": "makro",
      "passwordA": "KalaNai2",
      "status": true
    }]
      

  )
  db.flights.insertMany(
    [{
        "_id": {
          "$oid": "632be533b4e4702a0a78a4d1"
        },
        "depart": "Athens",
        "arrival": "Paris",
        "price": 300,
        "duration": "2",
        "date": "2022-03-04",
        "time": "03-45",
        "code": "AP22030403",
        "seats": 218
      },{
        "_id": {
          "$oid": "632be563b4e4702a0a78a4d2"
        },
        "depart": "Thesaloniki",
        "arrival": "Athens",
        "price": 80,
        "duration": "1",
        "date": "2022-03-09",
        "time": "12-35",
        "code": "TA22030912",
        "seats": 219
      },{
        "_id": {
          "$oid": "632d67b812730b102cf59a34"
        },
        "depart": "Kerkyra",
        "arrival": "Crete",
        "price": 250,
        "duration": "1",
        "date": "2022-06-27",
        "time": "13-50",
        "code": "KC22062713",
        "seats": 220
      }]
      

  )
  db.reservations.insertMany(
    [{
        "_id": {
          "$oid": "632d65f412730b102cf59a32"
        },
        "username": "Mary",
        "price": 300,
        "flightCode": "AP22030403",
        "ticket_code": "66847",
        "name": "mary",
        "passport": "1234",
        "credit_card": "1234567899098765",
        "created_date": {
          "$date": {
            "$numberLong": "1663930404000"
          }
        },
        "departT": "Athens",
        "arrivalT": "Paris",
        "dateT": "2022-03-04",
        "timeT": "03-45"
      },{
        "_id": {
          "$oid": "632d661d12730b102cf59a33"
        },
        "username": "Mary",
        "price": 80,
        "flightCode": "TA22030912",
        "ticket_code": "82373",
        "name": "mary",
        "passport": "1234",
        "credit_card": "1234567890987654",
        "created_date": {
          "$date": {
            "$numberLong": "1663930445000"
          }
        },
        "departT": "Thesaloniki",
        "arrivalT": "Athens",
        "dateT": "2022-03-09",
        "timeT": "12-35"
      },{
        "_id": {
          "$oid": "632dbc0c5e8dabcf67dbfa7c"
        },
        "username": "jaywalker",
        "price": 300,
        "flightCode": "AP22030403",
        "ticket_code": "16232",
        "name": "Giwrgos",
        "passport": "1234567898",
        "credit_card": "5555234816985341",
        "created_date": {
          "$date": {
            "$numberLong": "1663952444000"
          }
        },
        "departT": "Athens",
        "arrivalT": "Paris",
        "dateT": "2022-03-04",
        "timeT": "03-45"
      }]
      

  )







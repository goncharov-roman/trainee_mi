db.createUser(
    {
        user: "Roman",
        pwd: "1",
        roles: [
            {
                role: "readWrite",
                db: "mydb"
            }
        ]
    }
)
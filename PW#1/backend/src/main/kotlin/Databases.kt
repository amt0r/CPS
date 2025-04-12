package com.example

import org.jetbrains.exposed.sql.*

fun configureDatabases(): Database {
    val database = Database.connect(
        url = "jdbc:mysql://localhost:3306/multiphasemeter",
        user = "root",
        driver = "com.mysql.cj.jdbc.Driver",
        password = "new_password",
    )
    return database
}

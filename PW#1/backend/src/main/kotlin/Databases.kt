package com.example

import io.ktor.server.application.*
import org.jetbrains.exposed.sql.*

fun Application.configureDatabases(): Database {
    val database = Database.connect(
        url = "jdbc:mysql://localhost:3306/multiphasemeter",
        user = "root",
        driver = "com.mysql.cj.jdbc.Driver",
        password = "new_password",
    )
    return database
}

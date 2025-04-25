package com.example

import com.example.models.*
import io.ktor.http.*
import io.ktor.server.application.*
import io.ktor.server.http.content.*
import io.ktor.server.request.*
import io.ktor.server.response.*
import io.ktor.server.routing.*
import org.jetbrains.exposed.sql.*

fun Application.configureRouting(database: Database) {
    val meterService = MeterService(database)
    val historyService = HistoryService(database)
    val punishmentService = PunishmentService(database)
    val tariffService = TariffService(database)

    routing {
        staticResources("/", "static")

        route("/meters") {
            post("/") {
                val meterNewValues = call.receive<ExposedMeterValues>()
                val result = meterService.processMeterValues(meterNewValues, punishmentService, tariffService, historyService)
                call.respond(HttpStatusCode.OK, result)
            }

            get("/") {
                val meters = meterService.getAllMeters()
                call.respond(HttpStatusCode.OK, meters)
            }
        }

        route("/history") {
            get("/") {
                val historyList = historyService.getAllHistory()
                call.respond(HttpStatusCode.OK, historyList)
            }
        }

        route("/punishments") {
            get("/") {
                val punishment = punishmentService.read()
                if (punishment != null) {
                    call.respond(HttpStatusCode.OK, punishment)
                } else {
                    call.respond(HttpStatusCode.NotFound, "Punishment not found")
                }
            }
        }

        route("/tariffs") {
            get("/") {
                val tariff = tariffService.read()
                if (tariff != null) {
                    call.respond(HttpStatusCode.OK, tariff)
                } else {
                    call.respond(HttpStatusCode.NotFound, "Tariff not found")
                }
            }
        }
    }
}

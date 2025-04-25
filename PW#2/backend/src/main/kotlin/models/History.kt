package com.example.models

import kotlinx.coroutines.Dispatchers
import kotlinx.serialization.Serializable
import org.jetbrains.exposed.dao.id.IntIdTable
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.transactions.experimental.newSuspendedTransaction
import org.jetbrains.exposed.sql.transactions.transaction

@Serializable
data class ExposedHistory(
    val meterId: Int,
    val date: String,
    val day: Int,
    val night: Int,
    val charge: Int
)

class HistoryService(database: Database) {
    object History : IntIdTable() {
        val meterId = reference("meterId", MeterService.Meters)
        val date = varchar("dateOfCharge", 50)
        val day = integer("dayValue")
        val night = integer("nightValue")
        val charge = integer("charge")
    }

    init {
        transaction(database) {
            SchemaUtils.create(History)
        }
    }

    suspend fun getAllHistory(): List<ExposedHistory> {
        return dbQuery {
            History.selectAll()
                .map { ExposedHistory(it[History.meterId].value, it[History.date], it[History.day], it[History.night], it[History.charge]) }
        }
    }

    suspend fun addHistory(history: ExposedHistory): Int {
        return dbQuery {
            History.insertAndGetId {
                it[meterId] = history.meterId
                it[date] = history.date
                it[day] = history.day
                it[night] = history.night
                it[charge] = history.charge
            }.value
        }
    }

    private suspend fun <T> dbQuery(block: suspend () -> T): T =
        newSuspendedTransaction(Dispatchers.IO) { block() }
}

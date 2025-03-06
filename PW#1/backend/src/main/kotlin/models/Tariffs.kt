package com.example.models

import kotlinx.coroutines.Dispatchers
import kotlinx.serialization.Serializable
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.transactions.experimental.newSuspendedTransaction
import org.jetbrains.exposed.sql.transactions.transaction

@Serializable
data class ExposedTariff(
    val dayTariff: Int,
    val nightTariff: Int
)

class TariffService(database: Database) {
    object Tariffs : Table() {
        val day = integer("dayTariff")
        val night = integer("nightTariff")
    }

    init {
        transaction(database) {
            SchemaUtils.create(Tariffs)
        }
    }

    suspend fun create(tariff: ExposedTariff) {
        dbQuery {
            Tariffs
                .insert {
                    it[day] = tariff.dayTariff
                    it[night] = tariff.nightTariff
                }
        }
    }

    suspend fun read(): ExposedTariff? {
        return dbQuery {
            Tariffs.selectAll()
                .map { ExposedTariff(it[Tariffs.day], it[Tariffs.night]) }
                .singleOrNull()
        }
    }

    suspend fun update(tariff: ExposedTariff) {
        dbQuery {
            Tariffs.update({ Op.TRUE }) {
                it[day] = tariff.dayTariff
                it[night] = tariff.nightTariff
            }
        }
    }

    private suspend fun <T> dbQuery(block: suspend () -> T): T =
        newSuspendedTransaction(Dispatchers.IO) { block() }
}

package com.example.models

import kotlinx.coroutines.Dispatchers
import kotlinx.serialization.Serializable
import org.jetbrains.exposed.dao.id.IntIdTable
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.transactions.experimental.newSuspendedTransaction
import org.jetbrains.exposed.sql.transactions.transaction


@Serializable
data class ExposedPunishment(
    val dayPunishment: Int,
    val nightPunishment: Int
)

class PunishmentService(database: Database) {
    object Punishments : IntIdTable() {
        val day = integer("dayPunishment")
        val night = integer("nightPunishment")
    }

    init {
        transaction(database) {
            SchemaUtils.create(Punishments)
        }
    }

    suspend fun create(punishment: ExposedPunishment) {
        dbQuery {
            Punishments.insert {
                it[day] = punishment.dayPunishment
                it[night] = punishment.nightPunishment
            }
        }
    }

    suspend fun read(): ExposedPunishment? {
        return dbQuery {
            Punishments.selectAll()
                .map { ExposedPunishment(it[Punishments.day], it[Punishments.night]) }
                .singleOrNull()
        }
    }

    suspend fun update(punishment: ExposedPunishment) {
        dbQuery {
            Punishments.update({ Op.TRUE }) {
                it[day] = punishment.dayPunishment
                it[night] = punishment.nightPunishment
            }
        }
    }

    private suspend fun <T> dbQuery(block: suspend () -> T): T =
        newSuspendedTransaction(Dispatchers.IO) { block() }
}

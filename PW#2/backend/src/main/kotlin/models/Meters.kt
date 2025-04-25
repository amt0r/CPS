package com.example.models

import kotlinx.coroutines.Dispatchers
import kotlinx.serialization.Serializable
import org.jetbrains.exposed.dao.id.IntIdTable
import org.jetbrains.exposed.sql.*
import org.jetbrains.exposed.sql.SqlExpressionBuilder.eq
import org.jetbrains.exposed.sql.transactions.experimental.newSuspendedTransaction
import org.jetbrains.exposed.sql.transactions.transaction
import java.time.LocalDateTime
import java.time.format.DateTimeFormatter

@Serializable
data class ExposedMeterValues(
    val id: Int,
    var day: Int,
    var night: Int
)

@Serializable
data class ExposedMeter(
    val id: Int,
    val date: String,
    val day: Int,
    val night: Int,
    val lastCharge: Int
)

class MeterService(val database: Database) {
    object Meters : IntIdTable() {
        val date = varchar("lastDate",50)
        val day = integer("dayValue")
        val night = integer("nightValue")
        val lastCharge = integer("lastCharge")
    }

    init {
        transaction(database) {
            SchemaUtils.create(Meters)
        }
    }

    suspend fun create(meter: ExposedMeter): Int = dbQuery {
        Meters.insertAndGetId {
            it[id] = meter.id
            it[date] = meter.date
            it[day] = meter.day
            it[night] = meter.night
            it[lastCharge] = meter.lastCharge
        }.value
    }

    suspend fun read(id: Int): ExposedMeter? {
        return dbQuery {
            Meters.selectAll()
                .where { Meters.id eq id }
                .map { ExposedMeter(it[Meters.id].value, it[Meters.date], it[Meters.day], it[Meters.night], it[Meters.lastCharge]) }
                .singleOrNull()
        }
    }

    suspend fun update(id: Int, meter: ExposedMeter) {
        dbQuery {
            Meters.update({ Meters.id eq id }) {
                it[date] = meter.date
                it[day] = meter.day
                it[night] = meter.night
                it[lastCharge] = meter.lastCharge
            }
        }
    }

    suspend fun processMeterValues(
        meterNewValues: ExposedMeterValues,
        punishmentService: PunishmentService,
        tariffService: TariffService,
        historyService: HistoryService
    ): ExposedMeter {

        meterNewValues.day = maxOf(0, meterNewValues.day)
        meterNewValues.night = maxOf(0, meterNewValues.night)

        val meterOldValues = read(meterNewValues.id)
        val tariffs = tariffService.read()!!
        val punishments = punishmentService.read()!!
        val dateNow = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"))

        if (meterOldValues == null) {
            val charge = tariffs.dayTariff * meterNewValues.day + tariffs.nightTariff * meterNewValues.night
            val newMeter = ExposedMeter(
                id = meterNewValues.id,
                date = dateNow,
                day = meterNewValues.day,
                night = meterNewValues.night,
                lastCharge = charge
            )
            create(newMeter)

            historyService.addHistory(ExposedHistory(
                meterId = meterNewValues.id,
                date = dateNow,
                day = meterNewValues.day,
                night = meterNewValues.night,
                charge = charge
            ))

            return newMeter
        } else {
            if (meterNewValues.day < meterOldValues.day) meterNewValues.day = meterOldValues.day + punishments.dayPunishment
            if (meterNewValues.night < meterOldValues.night) meterNewValues.night = meterOldValues.night + punishments.nightPunishment

            val charge = tariffs.dayTariff * (meterNewValues.day - meterOldValues.day) + tariffs.nightTariff * (meterNewValues.night - meterOldValues.night)

            val updatedMeter = ExposedMeter(
                id = meterNewValues.id,
                date = dateNow,
                day = meterNewValues.day,
                night = meterNewValues.night,
                lastCharge = charge
            )

            historyService.addHistory(ExposedHistory(
                meterId = meterNewValues.id,
                date = dateNow,
                day = meterNewValues.day,
                night = meterNewValues.night,
                charge = charge
            ))

            update(meterNewValues.id, updatedMeter)
            return updatedMeter
        }
    }

    suspend fun getAllMeters(): List<ExposedMeter> {
        return dbQuery {
            Meters.selectAll()
                .map { ExposedMeter(it[Meters.id].value, it[Meters.date], it[Meters.day], it[Meters.night], it[Meters.lastCharge]) }
        }
    }

    private suspend fun <T> dbQuery(block: suspend () -> T): T =
        newSuspendedTransaction(Dispatchers.IO) { block() }
}


import com.example.models.*
import kotlinx.coroutines.runBlocking
import org.jetbrains.exposed.sql.Database
import org.jetbrains.exposed.sql.SchemaUtils
import org.jetbrains.exposed.sql.transactions.transaction
import org.junit.jupiter.api.Assertions.*
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.Test

class MeterServiceTest {
    private lateinit var meterService: MeterService
    private lateinit var punishmentService: PunishmentService
    private lateinit var tariffService: TariffService
    private lateinit var historyService: HistoryService

    private val DAY_TARIFF = 10
    private val NIGHT_TARIFF = 5
    private val DAY_PUNISHMENT = 100
    private val NIGHT_PUNISHMENT = 80

    @BeforeEach
    fun setup() {
        val database = Database.connect("jdbc:h2:mem:test;DB_CLOSE_DELAY=-1;", driver = "org.h2.Driver")

        transaction(database) {
            SchemaUtils.drop(MeterService.Meters, TariffService.Tariffs, PunishmentService.Punishments,
                HistoryService.History
            )
        }

        meterService = MeterService(database)
        punishmentService = PunishmentService(database)
        tariffService = TariffService(database)
        historyService = HistoryService(database)

        runBlocking {
            tariffService.create(ExposedTariff(DAY_TARIFF, NIGHT_TARIFF))
            punishmentService.create(ExposedPunishment(DAY_PUNISHMENT, NIGHT_PUNISHMENT))
        }
    }

    @Test
    fun `оновлення показників вже існуючого лічильника`() = runBlocking {
        val id = 1
        val dayValue = 90
        val nightValue = 40
        val differenceDay = 10
        val differenceNight = 15

        val oldMeter = ExposedMeter(id, "2024-02-27 12:00:00", dayValue, nightValue, 135)
        meterService.create(oldMeter)

        val meterValues = ExposedMeterValues(id, dayValue + differenceDay, nightValue + differenceNight)

        val result = meterService.processMeterValues(meterValues, punishmentService, tariffService, historyService)

        val expectedCharge = differenceDay * DAY_TARIFF + differenceNight * NIGHT_TARIFF

        assertEquals(dayValue + differenceDay, result.day)
        assertEquals(nightValue + differenceNight, result.night)
        assertEquals(expectedCharge, result.lastCharge)
    }

    @Test
    fun `отримання показників від нового лічильника`() = runBlocking {
        val id = 1
        val dayValue = 90
        val nightValue = 40

        val meterValues = ExposedMeterValues(id, dayValue, nightValue)

        val result = meterService.processMeterValues(meterValues, punishmentService, tariffService, historyService)

        val expectedCharge = dayValue * DAY_TARIFF + nightValue * NIGHT_TARIFF

        assertEquals(dayValue, result.day)
        assertEquals(nightValue, result.night)
        assertEquals(expectedCharge, result.lastCharge)
    }

    @Test
    fun `отримання показників з заниженими нічними показниками`() = runBlocking {
        val id = 1
        val dayValue = 90
        val nightValue = 40
        val differenceDay = 10
        val differenceNight = -15

        val oldMeter = ExposedMeter(id, "2024-02-27 12:00:00", dayValue, nightValue, 135)
        meterService.create(oldMeter)

        val meterValues = ExposedMeterValues(id, dayValue + differenceDay, nightValue + differenceNight)

        val result = meterService.processMeterValues(meterValues, punishmentService, tariffService, historyService)

        val expectedCharge = differenceDay * DAY_TARIFF + NIGHT_PUNISHMENT * NIGHT_TARIFF

        assertEquals(dayValue + differenceDay, result.day)
        assertEquals(nightValue + NIGHT_PUNISHMENT, result.night)
        assertEquals(expectedCharge, result.lastCharge)
    }

    @Test
    fun `отримання показників з заниженими денними показниками`() = runBlocking {
        val id = 1
        val dayValue = 90
        val nightValue = 40
        val differenceDay = -10
        val differenceNight = 15

        val oldMeter = ExposedMeter(id, "2024-02-27 12:00:00", dayValue, nightValue, 135)
        meterService.create(oldMeter)

        val meterValues = ExposedMeterValues(id, dayValue + differenceDay, nightValue + differenceNight)

        val result = meterService.processMeterValues(meterValues, punishmentService, tariffService, historyService)

        val expectedCharge = DAY_PUNISHMENT * DAY_TARIFF + differenceNight * NIGHT_TARIFF

        assertEquals(dayValue + DAY_PUNISHMENT, result.day)
        assertEquals(nightValue + differenceNight, result.night)
        assertEquals(expectedCharge, result.lastCharge)
    }

    @Test
    fun `отримання показників з заниженими нічними та денними показниками`() = runBlocking {
        val id = 1
        val dayValue = 90
        val nightValue = 40
        val differenceDay = -10
        val differenceNight = -15

        val oldMeter = ExposedMeter(id, "2024-02-27 12:00:00", dayValue, nightValue, 135)
        meterService.create(oldMeter)

        val meterValues = ExposedMeterValues(id, dayValue + differenceDay, nightValue + differenceNight)

        val result = meterService.processMeterValues(meterValues, punishmentService, tariffService, historyService)

        val expectedCharge = DAY_PUNISHMENT * DAY_TARIFF + NIGHT_PUNISHMENT * NIGHT_TARIFF

        assertEquals(dayValue + DAY_PUNISHMENT, result.day)
        assertEquals(nightValue + NIGHT_PUNISHMENT, result.night)
        assertEquals(expectedCharge, result.lastCharge)
    }

    @Test
    fun `отримання від'ємних показників від нового лічильника`() = runBlocking {
        val id = 1
        val dayValue = -90
        val nightValue = -40
        val zero = 0

        val meterValues = ExposedMeterValues(id, dayValue, nightValue)

        val result = meterService.processMeterValues(meterValues, punishmentService, tariffService, historyService)

        val expectedCharge = dayValue * DAY_TARIFF + nightValue * NIGHT_TARIFF

        assertEquals(zero, result.day)
        assertEquals(zero, result.night)
        assertEquals(zero, result.lastCharge)
    }
}
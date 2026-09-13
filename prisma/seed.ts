import "dotenv/config";
import { PrismaPg } from "@prisma/adapter-pg";
import { PrismaClient } from "../generated/prisma/client";

const adapter = new PrismaPg({ connectionString: process.env.DATABASE_URL });
const prisma = new PrismaClient({ adapter });

const AIRPORTS = [
  { code: "DXB", name: "Dubai International Airport", city: "Dubai" },
  { code: "LHR", name: "London Heathrow Airport", city: "London" },
  { code: "JFK", name: "John F. Kennedy International Airport", city: "New York" },
  { code: "CDG", name: "Paris Charles de Gaulle Airport", city: "Paris" },
  { code: "IST", name: "Istanbul Airport", city: "Istanbul" },
  { code: "AMM", name: "Queen Alia International Airport", city: "Amman" },
];

const USERS = [
  { passport: "P1029384", name: "Layla Haddad" },
  { passport: "P5647382", name: "Omar Khalil" },
  { passport: "P9182736", name: "Sarah Whitfield" },
  { passport: "P3746251", name: "Daniel Mercier" },
  { passport: "P8273645", name: "Mert Yilmaz" },
  { passport: "P4516273", name: "Aisha Rahman" },
];

const FLIGHTS = [
  {
    number: "FA101",
    originId: "DXB",
    destinationId: "LHR",
    deptTime: "2026-10-01T08:00:00.000Z",
    arrivalTime: "2026-10-01T12:30:00.000Z",
    price: 450,
    currency: "USD",
  },
  {
    number: "FA102",
    originId: "DXB",
    destinationId: "LHR",
    deptTime: "2026-10-01T21:00:00.000Z",
    arrivalTime: "2026-10-02T01:30:00.000Z",
    price: 620,
    currency: "USD",
  },
  {
    number: "FA103",
    originId: "LHR",
    destinationId: "DXB",
    deptTime: "2026-10-02T10:00:00.000Z",
    arrivalTime: "2026-10-02T19:15:00.000Z",
    price: 480,
    currency: "USD",
  },
  {
    number: "FA104",
    originId: "DXB",
    destinationId: "JFK",
    deptTime: "2026-10-03T02:30:00.000Z",
    arrivalTime: "2026-10-03T08:45:00.000Z",
    price: 890,
    currency: "USD",
  },
  {
    number: "FA105",
    originId: "JFK",
    destinationId: "DXB",
    deptTime: "2026-10-04T22:00:00.000Z",
    arrivalTime: "2026-10-05T19:30:00.000Z",
    price: 910,
    currency: "USD",
  },
  {
    number: "FA106",
    originId: "LHR",
    destinationId: "JFK",
    deptTime: "2026-10-02T09:00:00.000Z",
    arrivalTime: "2026-10-02T12:00:00.000Z",
    price: 390,
    currency: "USD",
  },
  {
    number: "FA107",
    originId: "LHR",
    destinationId: "JFK",
    deptTime: "2026-10-02T16:30:00.000Z",
    arrivalTime: "2026-10-02T19:30:00.000Z",
    price: 310,
    currency: "USD",
  },
  {
    number: "FA108",
    originId: "JFK",
    destinationId: "LHR",
    deptTime: "2026-10-05T19:00:00.000Z",
    arrivalTime: "2026-10-06T07:00:00.000Z",
    price: 420,
    currency: "USD",
  },
  {
    number: "FA109",
    originId: "CDG",
    destinationId: "IST",
    deptTime: "2026-10-03T07:20:00.000Z",
    arrivalTime: "2026-10-03T12:05:00.000Z",
    price: 210,
    currency: "USD",
  },
  {
    number: "FA110",
    originId: "IST",
    destinationId: "CDG",
    deptTime: "2026-10-06T13:40:00.000Z",
    arrivalTime: "2026-10-06T16:25:00.000Z",
    price: 235,
    currency: "USD",
  },
  {
    number: "FA111",
    originId: "AMM",
    destinationId: "DXB",
    deptTime: "2026-10-04T06:15:00.000Z",
    arrivalTime: "2026-10-04T10:05:00.000Z",
    price: 180,
    currency: "USD",
  },
  {
    number: "FA112",
    originId: "DXB",
    destinationId: "AMM",
    deptTime: "2026-10-07T23:45:00.000Z",
    arrivalTime: "2026-10-08T02:30:00.000Z",
    price: 195,
    currency: "USD",
  },
  {
    number: "FA113",
    originId: "IST",
    destinationId: "AMM",
    deptTime: "2026-10-05T11:10:00.000Z",
    arrivalTime: "2026-10-05T13:35:00.000Z",
    price: 160,
    currency: "USD",
  },
  {
    number: "FA114",
    originId: "CDG",
    destinationId: "LHR",
    deptTime: "2026-10-06T08:45:00.000Z",
    arrivalTime: "2026-10-06T09:05:00.000Z",
    price: 130,
    currency: "USD",
  },
  {
    number: "FA115",
    originId: "AMM",
    destinationId: "CDG",
    deptTime: "2026-10-08T09:30:00.000Z",
    arrivalTime: "2026-10-08T13:50:00.000Z",
    price: 340,
    currency: "USD",
  },
  {
    number: "FA116",
    originId: "LHR",
    destinationId: "CDG",
    deptTime: "2026-10-09T18:20:00.000Z",
    arrivalTime: "2026-10-09T20:35:00.000Z",
    price: 145,
    currency: "USD",
  },
];

const BOOKINGS = [
  { reference: "A1B2C3", flightNumber: "FA101", passport: "P1029384", seat: "1A" },
  { reference: "D4E5F6", flightNumber: "FA101", passport: "P5647382", seat: "1B" },
  { reference: "G7H8J9", flightNumber: "FA101", passport: "P9182736", seat: "2C" },
  { reference: "K1L2M3", flightNumber: "FA104", passport: "P1029384", seat: "1A" },
  { reference: "N4P5Q6", flightNumber: "FA104", passport: "P5647382", seat: "1B" },
  { reference: "R7S8T9", flightNumber: "FA104", passport: "P9182736", seat: "1C" },
  { reference: "U1V2W3", flightNumber: "FA104", passport: "P3746251", seat: "2A" },
  { reference: "X4Y5Z6", flightNumber: "FA104", passport: "P8273645", seat: "2B" },
  { reference: "B7C8D9", flightNumber: "FA104", passport: "P4516273", seat: "2C" },
  { reference: "E1F2G3", flightNumber: "FA106", passport: "P3746251", seat: "1A" },
  { reference: "H4J5K6", flightNumber: "FA109", passport: "P1029384", seat: "1A" },
  { reference: "L7M8N9", flightNumber: "FA109", passport: "P5647382", seat: "1B" },
  { reference: "P1Q2R3", flightNumber: "FA109", passport: "P9182736", seat: "1C" },
  { reference: "S4T5U6", flightNumber: "FA109", passport: "P3746251", seat: "2A" },
  { reference: "V7W8X9", flightNumber: "FA109", passport: "P8273645", seat: "2B" },
  { reference: "Y1Z2A3", flightNumber: "FA112", passport: "P4516273", seat: "1C" },
  { reference: "C4D5E6", flightNumber: "FA112", passport: "P8273645", seat: "2A" },
];

async function main() {
  for (const airport of AIRPORTS) {
    await prisma.airport.upsert({
      where: { code: airport.code },
      update: { name: airport.name, city: airport.city },
      create: airport,
    });
  }

  const userIdByPassport = new Map<string, string>();
  for (const user of USERS) {
    const record = await prisma.user.upsert({
      where: { passport: user.passport },
      update: { name: user.name },
      create: user,
    });
    userIdByPassport.set(record.passport, record.id);
  }

  const flightIdByNumber = new Map<string, string>();
  for (const flight of FLIGHTS) {
    const data = {
      ...flight,
      deptTime: new Date(flight.deptTime),
      arrivalTime: new Date(flight.arrivalTime),
    };
    const record = await prisma.flight.upsert({
      where: { number: flight.number },
      update: data,
      create: data,
    });
    flightIdByNumber.set(record.number, record.id);
  }

  for (const booking of BOOKINGS) {
    const flightId = flightIdByNumber.get(booking.flightNumber);
    const userId = userIdByPassport.get(booking.passport);
    if (!flightId || !userId) {
      throw new Error(`Unresolved booking ${booking.reference}`);
    }
    await prisma.booking.upsert({
      where: { flightId_seat: { flightId, seat: booking.seat } },
      update: { userId, reference: booking.reference },
      create: { flightId, userId, seat: booking.seat, reference: booking.reference },
    });
  }

  const summary = await prisma.flight.findMany({
    select: { number: true, totalSeats: true, _count: { select: { bookings: true } } },
    orderBy: { number: "asc" },
  });

  console.log(`airports: ${AIRPORTS.length}, users: ${USERS.length}, flights: ${FLIGHTS.length}`);
  for (const flight of summary) {
    console.log(`${flight.number}: ${flight.totalSeats - flight._count.bookings}/${flight.totalSeats} seats free`);
  }
}

main()
  .catch((error) => {
    console.error(error);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });

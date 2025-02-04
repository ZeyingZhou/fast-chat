import { PrismaClient } from '@prisma/client/edge'
import { withAccelerate } from '@prisma/extension-accelerate'

declare global {
  var cachedPrisma: ReturnType<typeof prismaClientSingleton>
}

const prismaClientSingleton = () => {
  return new PrismaClient().$extends(withAccelerate())
}

export const db = globalThis.cachedPrisma ?? prismaClientSingleton()

if (process.env.NODE_ENV !== "production") globalThis.cachedPrisma = db
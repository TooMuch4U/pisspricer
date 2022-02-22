import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const cors = {
    "origin": "http://localhost:8081",
    "methods": "GET,HEAD,PUT,PATCH,POST,DELETE,OPTIONS",
    "preflightContinue": false,
    "optionsSuccessStatus": 204,
    // "allowedHeaders": ['Origin', 'X-Requested-With', 'Content-Type', 'Accept', 'X-Authorization'],
    "credentials": true
  }
  const app = await NestFactory.create(AppModule, { cors } );
  app.setGlobalPrefix('scrapi/v1');
  await app.listen(3000);
}
bootstrap();

import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { SyncsModule } from './syncs/syncs.module';
import { AuthModule } from './auth/auth.module';
import {ConfigModule} from "@nestjs/config";

@Module({
  imports: [SyncsModule, AuthModule, ConfigModule.forRoot()],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}

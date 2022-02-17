import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { SyncsModule } from './syncs/syncs.module';

@Module({
  imports: [SyncsModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}

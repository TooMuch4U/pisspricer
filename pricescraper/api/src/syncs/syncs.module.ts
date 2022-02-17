import { Module } from '@nestjs/common';
import { SyncsService } from './syncs.service';
import { SyncsController } from './syncs.controller';

@Module({
  controllers: [SyncsController],
  providers: [SyncsService]
})
export class SyncsModule {}

import { Controller, Get, Post, Body, Patch, Param, Delete } from '@nestjs/common';
import { SyncsService } from './syncs.service';
import { CreateSyncDto } from './dto/create-sync.dto';
import { UpdateSyncDto } from './dto/update-sync.dto';

@Controller('syncs')
export class SyncsController {
  constructor(private readonly syncsService: SyncsService) {}

  @Get()
  findAll() {
    return this.syncsService.findAll();
  }

  @Get(':id')
  findOne(@Param('id') id: string) {
    return this.syncsService.findOne(id);
  }
}

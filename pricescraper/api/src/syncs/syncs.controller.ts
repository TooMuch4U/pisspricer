import {Controller, Get, Post, Body, Patch, Param, Delete, UseGuards, UseFilters, Query} from '@nestjs/common';
import { SyncsService } from './syncs.service';
import { CreateSyncDto } from './dto/create-sync.dto';
import { UpdateSyncDto } from './dto/update-sync.dto';
import {AuthGuard} from "@nestjs/passport";
import {BasicAuthExceptionFilter} from "../filters/basic-auth.filter";

@Controller('syncs')
export class SyncsController {
  constructor(private readonly syncsService: SyncsService) {}

  @Get()
  @UseGuards(AuthGuard('basic'))
  @UseFilters(BasicAuthExceptionFilter)
  findAll() {
    return this.syncsService.findAll();
  }

  @Get(':id')
  @UseGuards(AuthGuard('basic'))
  @UseFilters(BasicAuthExceptionFilter)
  findOne(
      @Param('id') id: string,
      @Query('failPage') failPage: number) {
    if (failPage == null) {
      failPage = 1
    }
    return this.syncsService.findOne(id, failPage);
  }
}

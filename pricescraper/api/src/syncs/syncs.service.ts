import {HttpException, HttpStatus, Injectable} from '@nestjs/common';
import { getDirectories } from '../utils/fs-helper';
import constants from '../utils/constants';
import {Sync} from "./entities/sync.entity";
const fs = require("fs");
import { promises as fspromise } from "fs";
const path = require('path')

@Injectable()
export class SyncsService {

  async findAll(): Promise<Sync[]> {
    let syncs = await getDirectories(constants.SYNC_SUMMARY_DIR);
    return syncs.map(datetime => {return {id: datetime}})
  }

  async getJsonFileIfExists(filePath): Promise<object[]> {
    let result = []
    if (fs.existsSync(filePath)) {
      const content = (await fspromise.readFile(filePath, "utf8"))
      result = JSON.parse("[" + content + "]")
    }
    return result
  }

  async findOne(id: string): Promise<Sync> {
    let sync = (await this.findAll()).find(sync => sync.id === id)

    // check the sync exists
    const syncPath = path.join(constants.SYNC_SUMMARY_DIR, id);
    if (!fs.existsSync(syncPath)) {
      throw new HttpException("Sync doesn't exist", HttpStatus.NOT_ACCEPTABLE);
    }

    // get all brands in sync
    let brandIds = await getDirectories(syncPath);
    sync.brands = await Promise.all(brandIds.map(async brandId => {

      // get the json paths
      const failPath = path.join(syncPath, brandId, constants.FAIL_FILE_NAME)
      const successPath = path.join(syncPath, brandId, constants.SUCCESS_FILE_NAME)
      const infoPath = path.join(syncPath, brandId, constants.INFO_FILE_NAME)

      // get fails and successes
      const fails = await this.getJsonFileIfExists(failPath);
      const successes = await this.getJsonFileIfExists(successPath);
      const info = await this.getJsonFileIfExists(infoPath);

      return {
        id: brandId,
        failsCount: fails.length,
        successCount: successes.length,
        fails,
        successes,
        ...(info[0])
      }
    }));

    return sync
  }
}

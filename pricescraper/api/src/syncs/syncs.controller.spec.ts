import { Test, TestingModule } from '@nestjs/testing';
import { SyncsController } from './syncs.controller';
import { SyncsService } from './syncs.service';

describe('SyncsController', () => {
  let controller: SyncsController;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      controllers: [SyncsController],
      providers: [SyncsService],
    }).compile();

    controller = module.get<SyncsController>(SyncsController);
  });

  it('should be defined', () => {
    expect(controller).toBeDefined();
  });
});

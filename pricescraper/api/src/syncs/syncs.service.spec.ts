import { Test, TestingModule } from '@nestjs/testing';
import { SyncsService } from './syncs.service';

describe('SyncsService', () => {
  let service: SyncsService;

  beforeEach(async () => {
    const module: TestingModule = await Test.createTestingModule({
      providers: [SyncsService],
    }).compile();

    service = module.get<SyncsService>(SyncsService);
  });

  it('should be defined', () => {
    expect(service).toBeDefined();
  });
});

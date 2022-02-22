
export interface Sync {
    id: string;
    brands?: BrandSync[]
}

export interface BrandSync {
    id: number;
    successCount: number;
    failCount: number;
    fails: object[];
    successes: object[];
    startTime: string;
    endTime: string;
}


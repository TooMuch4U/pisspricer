
class NonExistentRegionException extends Error {
    constructor(message) {
        super(message);
        this.name = "NonExistentRegionException";
    }
}
exports.NonExistentRegionException = NonExistentRegionException;

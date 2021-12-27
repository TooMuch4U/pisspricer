
class NonExistentBrandException extends Error {
    constructor(message) {
        super(message);
        this.name = "NonExistentBrandException";
    }
}
exports.NonExistentBrandException = NonExistentBrandException;


class ItemDoesntExistException extends Error {
    constructor(message) {
        super(message);
        this.name = "ItemDoesntExistException";
    }
}
exports.ItemDoesntExistException = ItemDoesntExistException;

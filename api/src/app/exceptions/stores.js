/**
 * For when a stores internal ID is not unique
 */
class NoneUniqueInternalStoreIdException extends Error {
    constructor(message) {
        super(message);
        this.name = "NoneUniqueInternalStoreIdException";
    }
}

exports.NoneUniqueInternalStoreIdException = NoneUniqueInternalStoreIdException;


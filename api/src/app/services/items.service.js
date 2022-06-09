const tools = require( "../services/tools");
const Items = require( "../models/items.model");
const Images = require( "../models/images.model");
const ItemsModel = require( '../models/items.model');
const Prices = require( "../models/itemPrices.model");
const {ItemDoesntExistException} = require( "../exceptions/items");

/**
 * Gets the item with matching internalSku
 * @param internalSku
 * @param brandId
 * @returns {Promise<null|*|undefined>}
 */
async function getItemByInternalSku(internalSku, brandId) {
    return await ItemsModel.getByInternalSku(internalSku, brandId)
}
exports.getItemByInternalSku = getItemByInternalSku;

async function create(newItem, barcodes = null, connection = null) {
    let slugName = newItem.name + (typeof newItem.volumeEach == 'undefined' ? '' : newItem.volumeEach);
    return await Items.insertWithBarcodeList(
        tools.toUnderscoreCase(newItem),
        barcodes ? barcodes : [],
        slugName,
        connection);
}
exports.create = create;

async function setImage(sku, image) {
    // get item form sku
    const item = await ItemsModel.getBySku(sku);

    // save image
    const path = `items/`;
    const blob = {"originalname": sku, "buffer": image};
    await Images.uploadImage(blob, path);

    // set image flag
    if (item.hasImage !== 1) {
        await Items.setImage(sku, 1);
    }
}
exports.setImage = setImage;

/**
 * Gets the item by sku.
 * Returns null if it doesn't exist
 * @param sku Sku of item to get
 * @param connection
 * @returns {Promise<null|*|undefined>} The item, if it exists.
 */
async function getBySku(sku, connection = null) {
    return await ItemsModel.getBySku(sku, connection);
}
exports.getBySku = getBySku;

/**
 * Checks the item exists and returns if the price was new or not.
 * @param sku
 * @param storeId
 * @param newItemPrice
 * @returns {Promise<boolean|undefined>}
 */
async function setOrUpdatePrice(sku, storeId, newItemPrice) {
    // Check if sku exists
    const item = await getBySku(sku);
    if (!item) {
        throw new ItemDoesntExistException(`Item with SKU '${sku}' doesn't exist`);
    }

    // Insert price
    return await Prices.insertOrSetPrice(sku, storeId, newItemPrice);
}
exports.setOrUpdatePrice = setOrUpdatePrice;

exports.getAllForBrand = async function (brandId) {
    return await ItemsModel.getAllForBrand(brandId);
}

async function combineAllSkus(skus, connection) {
    const skuToKeep = skus[0];
    const otherSkus = skus.slice(1)
    const item = await ItemsModel.getBySku(skuToKeep, connection)
    const data = {name: item.name};
    for (const sku of otherSkus) {
        await ItemsModel.combineItems(skuToKeep, sku, data, true, connection);
    }
    return skuToKeep;
}

async function addBarcodesToSku(barcodes, sku, connection = null) {
    const allBarcodes = await ItemsModel.allBarcodes(connection);
    barcodes = barcodes.filter(barcode => !allBarcodes.map(code => code.ean).includes(barcode))
    for (const barcode of barcodes) {
        await ItemsModel.insertBarcode(sku, barcode, connection);
    }
}

async function createOrGetItem(internalSku, brandId, newItem, barcodes) {
    const transactionConn = await Items.createTransaction();
    try {
        let item = await ItemsModel.getByInternalSku(internalSku, brandId, transactionConn);

        // try find from barcodes
        if (!item) {
            const skus = await ItemsModel.getSkusAssociatedWithBarcodes(barcodes, transactionConn);
            if (skus.length > 1) {
                const sku = await combineAllSkus(skus, transactionConn);
                await addBarcodesToSku(barcodes, sku, transactionConn);
                item = await ItemsModel.getBySku(sku, transactionConn);
            }
            else if (skus.length === 1) {
                await addBarcodesToSku(barcodes, skus[0], transactionConn);
                item = await ItemsModel.getBySku(skus[0], transactionConn);
            }
        }

        // item doesn't exist
        // if (!item) {
        //     item = await ItemsModel.getByBarcodes(barcodes, transactionConn);
        // }
        let itemCreated = false;
        if (!item) {
            const sku = await create(newItem, barcodes, transactionConn);
            item = await getBySku(sku, transactionConn);
            itemCreated = true;
        }

        await Items.commitTransaction(transactionConn);

        return {
            item,
            itemCreated
        }
    }
    catch (e) {
        await Items.rollbackTransaction(transactionConn);
        throw e
    }
    finally {
        await Items.releaseTransaction(transactionConn);
    }

}
exports.createOrGetItem = createOrGetItem;
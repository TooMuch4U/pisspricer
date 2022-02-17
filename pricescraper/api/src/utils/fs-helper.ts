const { promises: { readdir } } = require('fs')

export async function getDirectories(source: string) {
    return (await readdir(source, {withFileTypes: true}))
        .filter(dirent => dirent.isDirectory())
        .map(dirent => dirent.name)
}

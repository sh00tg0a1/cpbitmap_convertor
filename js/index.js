const fs = require('fs')
const util = require('util')

const Jimp = require('jimp')

const main = async () => {
    if (process.argv.length != 4) {
        console.log('Need two args: input filename and result filename')
        console.log(`Example: ${process.argv[0]} ${process.argv[1]} HomeBackground.cpbitmap HomeBackground.png`)
        return
    }

    const inpFileName = process.argv[2]
    const outFileName = process.argv[3]

    const readFile = util.promisify(fs.readFile)

    const cpbmp = await readFile(inpFileName)
    const width = cpbmp.readInt32LE(cpbmp.length - 4 * 5)
    const height = cpbmp.readInt32LE(cpbmp.length - 4 * 4)

    console.log(`Image height: ${height}, width: ${width}`)

    const image = await new Jimp(width, height, 0x000000FF)

    const calcOffsetInCpbmp = (x, y, width) => {
        const lineSize = Math.ceil(width / 16) * 16
        console.log(x, y, lineSize)
        return x * 4 + y * lineSize * 4
    }

    const calcOffsetInImage = (x, y, width) => {
        return x * 4 + y * width * 4
    }

    const swapRBColors = (c) => {
        const r = c & 0xFF
        const b = (c & 0xFF0000) >> 16
        c &= 0xFF00FF00
        c |= r << 16
        c |= b
        return c
    }

    for (let y = 0; y < height; y++) {
        for (let x = 0; x < width; x++) {
            const color = cpbmp.readInt32LE(calcOffsetInCpbmp(x, y, width))
            image.bitmap.data.writeInt32LE(swapRBColors(color), calcOffsetInImage(x, y, width))
        }
    }

    await image.write(outFileName)

    console.log('Done')
}

main()
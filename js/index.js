const fs = require('fs').promises

const Jimp = require('jimp')

const main = async () => {
    if (process.argv.length !== 4) {
        console.log('Need two args: input filename and result filename')
        console.log(`Example: ${process.argv[0]} ${process.argv[1]} HomeBackground.cpbitmap HomeBackground.png`)
        return
    }

    const inpFileName = process.argv[2]
    const outFileName = process.argv[3]

    const cpbmp = await fs.readFile(inpFileName)
    const width = cpbmp.readInt32LE(cpbmp.length - 4 * 5)
    const height = cpbmp.readInt32LE(cpbmp.length - 4 * 4)

    console.log(`Image height: ${height}, width: ${width}`)

    const image = await new Jimp(width, height, 0x000000ff)

    const stride = Math.ceil(width / 16) * 16 * 4
    const calcOffsetInCpbmp = (x, y) => x * 4 + y * stride
    const calcOffsetInImage = (x, y) => (x + y * width) * 4

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
            const color = cpbmp.readUInt32LE(calcOffsetInCpbmp(x, y))
            image.bitmap.data.writeInt32LE(swapRBColors(color), calcOffsetInImage(x, y))
        }
    }

    await image.write(outFileName)

    console.log('Done')
}

main()

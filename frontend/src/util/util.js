const percentToHex = (p) =>{
    let percent = Math.max(0, Math.min(100, p)) // bound percent from 0 to 100
    let decimalVal = Math.round(percent / 100 * 255)   // convert to decimal
    let hexValue = decimalVal.toString(16)  // get hexadecimal representation
    return hexValue.padStart(2, '0').toUpperCase(); // format with the leading zero and upper case
}

// color should be represented in hex
const setColorOpacity = (color, opacity) =>{
    return color + percentToHex(opacity)
}

export default setColorOpacity
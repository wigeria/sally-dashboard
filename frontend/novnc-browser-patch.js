// Mock the browser detection functions
export const isMac = navigator.platform.indexOf('Mac') !== -1;
export const isWindows = navigator.platform.indexOf('Win') !== -1;
export const isIOS = /iPad|iPhone|iPod/.test(navigator.platform);
export const isAndroid = navigator.userAgent.indexOf('Android') !== -1;
export const isSafari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
export const isFirefox = navigator.userAgent.indexOf('Firefox') !== -1;
export const supportsWebCodecsH264Decode = false; // Set default to false

// Other browser detection functions as needed
import moment from 'moment'

/**
 * Takes a date string and parses into date object
 * Format: dd.MM.yyyy HH:mm:ss.SSSSSS
 * @param unparsedStr
 * @returns {Date}
 */
export function parseDate (unparsedStr) {
  const momentDate = moment(unparsedStr, 'YYYY-MM-DD HH:mm:ss.SSSSSS')
  return momentDate.toDate()
}

/**
 * Takes an un-parsed date string and returns the date as a formatted string
 * eg. "Web Feb 16 2022 2:31 PM"
 * @param unparsedStr
 * @returns {string}
 */
export function getDateString (unparsedStr) {
  const date = parseDate(unparsedStr)
  const time = date.toLocaleString('en-US', {
    hour: 'numeric', hour12: true, minute: 'numeric' })
  return date.toDateString() + ' ' + time
}

/**
 * Takes a time in milliseconds and returns a formatted string.
 * eg. 1800 -> "3m"
 * @param diffMs Difference in time (milliseconds)
 * @returns {string}
 */
function formatDiff (diffMs) {
  const diffDays = Math.floor(diffMs / 86400000)
  const diffHrs = Math.floor((diffMs % 86400000) / 3600000)
  const diffMins = Math.round(((diffMs % 86400000) % 3600000) / 60000)

  let timeStr = `${diffMins}m`
  if (diffHrs > 0) {
    timeStr = `${diffHrs}h ${timeStr}`
  }
  if (diffDays > 0) {
    timeStr = `${diffDays}d ${timeStr}`
  }

  return timeStr
}

/**
 * Takes two un-parsed date strings and returns the time difference between
 * eg. "2h 15m"
 * @param start First date (unparsed string)
 * @param end Second date (unparsed string)
 * @returns {string} Time difference between two dates
 */
export function getTimeDiffFormatted (start, end) {
  const diffMs = parseDate(end) - parseDate(start)
  return formatDiff(diffMs)
}

/**
 * Takes an un-parsed date string from past and returns the time difference between now and then
 * eg. "2h 15m"
 * @param date Date to compare (unparsed string)
 * @returns {string} Time difference between now and the date
 */
export function getTimeSinceNowFormatted (date) {
  const now = new Date()
  const diffMs = now - parseDate(date)
  return formatDiff(diffMs)
}

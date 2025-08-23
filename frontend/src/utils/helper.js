export const formatConversationTime = (dateString) => {
    const messageDate = new Date(dateString);
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    const yesterday = new Date(today)
    yesterday.setDate(today.getDate() - 1)
   
    const nowUnix = now.valueOf()
    const oneMinute = 60000
    
    const dayInMilliseconds = (oneMinute * 60) * 24
    const weekInMilliseconds = (dayInMilliseconds * 7)
    const oneMinuteAgo = (nowUnix - oneMinute)
    const oneHourAgo = (nowUnix - (oneMinute * 60))
    const oneWeekAgo = (nowUnix - weekInMilliseconds)
    const messageDateUnix = messageDate.valueOf()

    const dateMoreThanOneWeek = messageDate.toLocaleDateString(undefined, { 
    year: "numeric", 
    month: "short", 
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit"
    })

    const dateThisWeek = messageDate.toLocaleDateString(undefined, {
        weekday: "long",
        hour: "2-digit",
        minute: "2-digit"
    })

    const timeFormat = messageDate.toLocaleTimeString(undefined, {
        hour: "2-digit",
        minute: "2-digit"
    })


    if (messageDateUnix <= oneWeekAgo) {
        return dateMoreThanOneWeek
    } else if (messageDate < yesterday ) {
        return dateThisWeek
    } else if (messageDate < today ) {
        return `Yesterday, ${timeFormat}`
    } else if (messageDateUnix < oneHourAgo) {
        return `Today, ${timeFormat}`
    } else if (messageDateUnix < oneMinuteAgo) {
        const minutesAgo = Math.floor((nowUnix - messageDateUnix) / oneMinute)
        return `${minutesAgo} minutes ago`
    } else {
        return "Just Now"
    }

};
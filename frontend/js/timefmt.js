function fmtTime(timestamp) {
    // remove microseconds if present, because JS Date can't parse them reliably
    const cleanTs = timestamp.split('.')[0] + 'Z'; // ensures UTC format
    const d = new Date(cleanTs);

    // Format to "Aug 21 2025 11:58:19 PM"
    const options = {
        year: 'numeric',
        month: 'short',
        day: '2-digit',
        hour: 'numeric',
        minute: '2-digit',
        second: '2-digit',
        hour12: true,
    };

    return new Intl.DateTimeFormat('en-US', options).format(d);
}

let serversToApprove = [];

function addToApprovedServers(serverId) {
    if serversToApprove.contains(serverId) {
        const index = serversToApprove.indexOf(serverId)
        serversToApprove.splice(index, 1)
        return
    }
    serversToApprove.push(serverId);
}

function sendSelectedServers() {
    const response = fetch("/server/approve", {
        method: "POST",
        mode: "cors",
        cache: "no-cache",
        headers: {
            "Content-Type": "application/json",
        },
        data={
           "server_ids": serversToApprove,
        },
        redirect: "follow"
    })
    serversToApprove = []
}

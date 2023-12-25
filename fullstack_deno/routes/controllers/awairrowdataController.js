import * as awairrowdataService from "../../services/awairrowdataService";

const listData = async () => {
    const data = {
        awairRow: await awairrowdataService.findAll(),
    };
    return new Response(await renderFile("index.eta", data), responseDetails);
};


export { listData }
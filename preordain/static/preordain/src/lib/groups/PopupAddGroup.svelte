<script lang="ts">
    import { connectURL } from "../../assets/stores";
    import type { PostGroupsNew } from "./interfaces";

    async function addNewGroup(params:PostGroupsNew) {
        await fetch(`${connectURL}/groups/delete`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "write": "testing"
            },
            body: JSON.stringify(params)
        }).then((data) => {
            if (data.status == 201) {
                return true
            }
            else {
                return false
            }
        })
    }
</script>

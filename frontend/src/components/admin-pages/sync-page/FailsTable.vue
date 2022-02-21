<template>
  <table>
    <!-- header -->
    <tr>
      <th>Image</th>
      <th>Response</th>
      <th>Store</th>
      <th>Location</th>
      <th>Item</th>
    </tr>

    <!-- content -->
    <tr
      v-for="fail in fails"
      v-bind:key="`${fail.item.itemPrice.internalSku}-${fail.item.store.internalId}`"
    >
      <!-- image -->
      <td>
        <img :alt="fail.item.item.name" class="small" :src="`data:image/png;base64,${fail.item.item.image}`" />
      </td>

      <!-- response -->
      <td>{{ fail.status }} {{ fail.message }}</td>

      <!-- store -->
      <td>
        {{ fail.item.store.name }}
        <p class="text-muted">({{ fail.item.store.internalId }})</p>
      </td>

      <!-- location -->
      <td class="text-left">
        Latitude: {{ fail.item.store.location.lattitude }}<br/>
        Longitude: {{ fail.item.store.location.longitude }}<br/>
        Address: {{ fail.item.store.location.address }}<br/>
        Region: {{ fail.item.store.location.region }}<br/>
        Postcode: {{ fail.item.store.location.postcode }}<br/>
      </td>

      <!-- item -->
      <td class="text-left">
        <strong>Name:</strong> {{ fail.item.item.name }} <span class="text-muted">
        ({{ fail.item.itemPrice.internalSku }})</span><br/>
        <strong>InternalSku:</strong> <br/>
        <strong>Price:</strong> {{ fail.item.itemPrice.price }}<br/>
        <strong>Sale Price:</strong> {{ fail.item.itemPrice.salePrice }}<br/>
        <strong>Stock:</strong> {{ fail.item.itemPrice.stock }}<br/>
      </td>
    </tr>
  </table>
</template>

<script>
export default {
  name: 'FailsTable',

  props: {
    fails: Array
  }
}
</script>

<style scoped>
.small {
  height: 50px;
}
</style>

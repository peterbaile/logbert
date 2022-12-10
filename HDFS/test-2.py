import random

vocab = {
  'mask_index': 2

}

random.seed(1234)

tokens = [random.randrange(70, 95) for _ in range(10000)]

print(tokens[:10])

add_special_tokens = False

new_tokens = []
output_label = []

def foo():
  for i, token in enumerate(tokens):
    if add_special_tokens:
      # if int(token) < 90:
      #   new_tokens.append(self.vocab.log_index)
      # else:
      #   new_tokens.append(self.vocab.scalar_index)
      
      output_label.append(0)
    
    prob = random.random()
    # replace 15% of tokens in a sequence to a masked token
    if prob < 0.65:
      # raise AttributeError("no mask in visualization")

      if True:
        # tokens[i] = self.vocab.mask_index
        output_label.append(token)

        # if self.add_special_tokens:
        #     new_tokens.append(self.vocab.mask_index)

        continue
    
    else:
      # tokens[i] = self.vocab.stoi.get(token, self.vocab.unk_index)
      
      # if self.add_special_tokens:
      #     new_tokens.append(self.vocab.stoi.get(token, self.vocab.unk_index))

      output_label.append(0)

  if add_special_tokens:
    return new_tokens, output_label

  return tokens, output_label

_, output = foo()


# print(tokens)
# print(output_label)

count = 0

for i in output:
  if i > 0:
    count += 1

print(count)